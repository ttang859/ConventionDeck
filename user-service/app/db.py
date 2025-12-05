import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, update

from .models import UserResponse

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
    email: str  # EmailStr
    username: str
    user_type: str  # Literal["vendor", "attendee"]

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Userdb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Userdb connection closed.")

# ORM function to create user instance in userdb table
def create_user_info(email, username, user_type):
    with Session(engine) as session, session.begin():
        user = UserInfo(
            email=email, username=username, user_type=user_type)
        session.add(user)
        session.commit()

# ORM function to retrieve user instance by email (early exposure, secure retrieval will use id from this call)
def get_user_info(user_email):
    with Session(engine) as session:
        statement = select(UserInfo).where(UserInfo.email == user_email)
        return session.exec(statement).one_or_none()

# ORM function to update username and user_type provided a user id
def update_user_info(id, username, user_type):
    with Session(engine) as session:
        value_hash = {}
        if username:
            value_hash["username"] = username
        if user_type:
            value_hash["user_type"] = user_type
        statement = update(UserInfo).where(UserInfo.id == id).values(
            value_hash)
        session.exec(statement)
        session.commit()
        user = session.exec(select(UserInfo).where(
            UserInfo.id == id)).one_or_none()
        if user:
            return UserResponse(id=user.id, email=user.email, username=user.username, user_type=user.user_type)# type: ignore

# ORM to delete user from userdb (need to consider cascading, hold for now)
def delete_user_info(user_id):
    with Session(engine) as session, session.begin():
        statement = select(UserInfo).where(UserInfo.id == user_id)
        user = session.exec(statement).one_or_none()
        if user:
            session.delete(user)
            session.commit()
            return "sucessful delete"
        return "nothing deleted"
