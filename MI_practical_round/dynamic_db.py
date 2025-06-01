import random

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import SQLModel, Session

from models.users_models import User


def get_tenant_db_url(org_name: str) -> str:
    return f"postgresql://postgres:postgres@localhost:5432/org_{org_name}"


def create_org_db_and_admin(org_name: str, admin_email: str):
    db_url = get_tenant_db_url(org_name)
    if not database_exists(db_url):
        create_database(db_url)

    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.create_all(engine)

    # Add admin user with dummy OTP
    otp = str(random.randint(100000, 999999))
    with Session(engine) as session:
        admin = User(email=admin_email, is_admin=True, otp=otp, password=otp)
        session.add(admin)
        session.commit()

    print(f"Tenant DB 'org_{org_name}' created with admin: {admin_email}, OTP: {otp}")
