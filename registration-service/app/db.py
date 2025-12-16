import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from sqlmodel import (Field, Session, SQLModel, and_, create_engine, delete,
                      select, update)

from .models import RegisteredPair

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


class Registration(SQLModel, table=True):
    __tablename__ = "registration"  # type: ignore # matches our table name in SQL

    conv_id: str = Field(primary_key=True)
    attendee_id: str = Field(primary_key=True)

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Conventiondb connection closed.")


def register_user(conv_id, attendee_id):
    with Session(engine) as session, session.begin():
        entry = Registration(conv_id=conv_id, attendee_id=attendee_id)
        session.add(entry)
        session.commit()


def unregister_user(conv_id, attendee_id):
    with Session(engine) as session, session.begin():
        statement = select(Registration).where(
            and_(Registration.conv_id == conv_id, Registration.attendee_id == attendee_id))
        entry = session.exec(statement).one_or_none()
        session.delete(entry)
        session.commit()


def get_convention_attendees(conv_id):
    with Session(engine) as session:
        statement = select(Registration).where(Registration.conv_id == conv_id)
        attendees = session.exec(statement)
        return list(map((lambda a: RegisteredPair(conv_id=a.conv_id, attendee_id=a.attendee_id).model_dump()), attendees))


def get_attending_conventions(attendee_id):
    with Session(engine) as session:
        statement = select(Registration).where(
            Registration.attendee_id == attendee_id)
        conventions = session.exec(statement)
        return list(map((lambda a: RegisteredPair(conv_id=a.conv_id, attendee_id=a.attendee_id).model_dump()), conventions))
