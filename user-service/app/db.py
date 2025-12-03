import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, update

# Load the Postgres DSN (connection string) from environment variables
DB = os.getenv("POSTGRES_DB")
SERVICE_NAME = os.getenv("POSTGRES_SERVICE")
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")
PSQL_PORT = int(os.getenv("POSTGRES_PORT", "5432"))


PG_DSN = os.getenv(
    "PG_DSN", f'postgresql+psycopg://{USER}:{PASS}@{SERVICE_NAME}:{PSQL_PORT}/{DB}')

# Create the SQLAlchemy engine that connects to your database
engine = create_engine(PG_DSN)

# define the UserInfo model — represents one table in Postgres


class UserInfo(SQLModel, table=True):
    __tablename__ = "user_info"  # type: ignore # matches our table name in SQL

    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr
    username: str
    user_type: str

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Userdb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Userdb connection closed.")


def create_user_info(email, username, user_type):
    with Session(engine) as session, session.begin():
        # if get_user_info(email) is not None:
            # statement = update(UserInfo).where(UserInfo.email == email).values(
            #     username=username, user_type=user_type)
            # user = session.exec(statement).one_or_none()
        # else:
        user = UserInfo(
            email=email, username=username, user_type=user_type)
        session.add(user)
        session.commit()

def get_user_info(user_email):
    with Session(engine) as session:
        statement = select(UserInfo).where(UserInfo.email == user_email)
        return session.exec(statement).first()

def update_user_info(email, username, user_type):
    with Session(engine) as session, session.begin():
        statement = update(UserInfo).where(UserInfo.email == email).values(
        username=username, user_type=user_type)
        user = session.exec(statement).one_or_none()
        session.commit()
        return user

def delete_user_info(user_id):
    with Session(engine) as session, session.begin():
        statement = select(UserInfo).where(UserInfo.id == user_id)
        user = session.exec(statement).one_or_none()
        if user:
            session.delete(user)
            session.commit()
            return "sucessful delete"
        return "nothing deleted"
