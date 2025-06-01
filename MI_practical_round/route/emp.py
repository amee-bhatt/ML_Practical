from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, select

from auth import create_access_token, ALGORITHM, SECRET_KEY
from dynamic_db import create_org_db_and_admin, get_tenant_db_url
from models.org_models import OrgCreate, RegisterOrganization, OrgGetRequest
from models.users_models import AdminLoginRequest, User, CreateUserWithTokenRequest
from postgres_conn import get_session

route = APIRouter()


@route.post("/register-org")
def register_org(
    org: OrgCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    existing = session.exec(
        select(RegisterOrganization).where(
            RegisterOrganization.org_name == org.org_name
        )
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    new_org = RegisterOrganization(**dict(org))
    session.add(new_org)
    session.commit()
    session.refresh(new_org)
    background_tasks.add_task(
        create_org_db_and_admin,
        org_name=org.org_name.lower(),  # e.g., org_acme
        admin_email=org.email,
    )

    return {
        "message": f"Organization '{org.org_name}' registered. Setting up the database in background."
    }


@route.post("/org/get")
def get_organization(payload: OrgGetRequest, session: Session = Depends(get_session)):
    org = session.exec(
        select(RegisterOrganization).where(
            RegisterOrganization.org_name == payload.organization_name
        )
    ).first()

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {"org_name": org.org_name, "owner_name": org.owner_name, "email": org.email}


@route.post("/login")
def login_admin(
    payload: AdminLoginRequest,
    master_session: Session = Depends(get_session),  # master DB session
):
    # 1. Check org in master DB
    org = master_session.exec(
        select(RegisterOrganization).where(RegisterOrganization.email == payload.email)
    ).first()

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # 2. Connect to tenant DB
    db_url = get_tenant_db_url(org.org_name)
    engine = create_engine(db_url)

    with Session(engine) as tenant_session:
        user = tenant_session.exec(
            select(User).where(
                User.email == org.email and User.password == payload.passowrd
            )
        ).first()

        if not user or not user.is_admin or user.password != payload.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.email, "org": org.org_name})

        return {"access_token": token, "token_type": "bearer"}


@route.post("/users/create")
def create_user(request: CreateUserWithTokenRequest):
    from jose import JWTError, jwt

    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_email = payload.get("sub")
        org_name = payload.get("org")

        if not admin_email or not org_name:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token decoding failed")

    # Connect to tenant DB
    db_url = get_tenant_db_url(org_name)
    engine = create_engine(db_url)

    with Session(engine) as session:
        # Check admin user
        admin = session.exec(select(User).where(User.email == admin_email)).first()
        if not admin or not admin.is_admin:
            raise HTTPException(status_code=403, detail="Only admins can create users")

        # Check if user already exists
        existing = session.exec(select(User).where(User.email == request.email)).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create user
        new_user = User(email=request.email, password=request.password, is_admin=False)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"message": "User created", "user": {"email": new_user.email}}
