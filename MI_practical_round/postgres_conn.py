from sqlmodel import create_engine, SQLModel, Session


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    from models.org_models import RegisterOrganization
    from models.users_models import User

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
