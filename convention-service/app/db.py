import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, update

from .models import ConventionCreate, ConventionResponse

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


class ConventionInfo(SQLModel, table=True):
    __tablename__ = "convention_info"  # type: ignore # matches our table name in SQL

    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    convention_name: str
    host_id: str
    loc: str
    start: datetime
    vendor_count: int = 0

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Conventiondb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Conventiondb connection closed.")


format = "%Y-%m-%d %H:%M:%S"


def create_convention(conv_name, host_id, loc, start_datetime):
    with Session(engine) as session, session.begin():
        entry = ConventionInfo(convention_name=conv_name,
                               host_id=host_id, loc=loc, start=start_datetime)
        id = entry.id
        session.add(entry)
        session.commit()
        return id


def get_convention_by(conv_id: str | None, host_id: str | None):
    with Session(engine) as session:
        if conv_id is None and host_id is None:
            statement = select(ConventionInfo)
        elif host_id:
            statement = select(ConventionInfo).where(
                ConventionInfo.host_id == host_id)
        else:
            statement = select(ConventionInfo).where(
                ConventionInfo.id == conv_id)
        conventions = session.exec(statement).all()
        return list(map(lambda c: ConventionResponse(id=c.id, convention_name=c.convention_name, host_id=c.host_id, start=c.start, loc=c.loc, vendor_count=c.vendor_count).model_dump(), conventions))


def update_convention(conv_id, start_datetime, loc, vendor_count):
    with Session(engine) as session, session.begin():
        value_map = {}
        if start_datetime:
            value_map["start"] = start_datetime
        if loc:
            value_map["loc"] = loc
        if vendor_count:
            value_map["vendor_count"] = vendor_count
        statement = update(ConventionInfo).where(
            ConventionInfo.id == conv_id).values(value_map)
        session.exec(statement)
        session.commit()


def delete_convention(conv_id):
    with Session(engine) as session, session.begin():
        statement = select(ConventionInfo).where(ConventionInfo.id == conv_id)
        entry = session.exec(statement).one_or_none()
        if entry:
            session.delete(entry)
            session.commit()
