import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from sqlmodel import (
    Field,
    Session,
    SQLModel,
    and_,
    create_engine,
    delete,
    select,
    update,
)

from .models import BoothAssignmentResp

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


class VendorBooths(SQLModel, table=True):
    __tablename__ = "vendor_booths"  # type: ignore # matches our table name in SQL

    conv_id: str = Field(primary_key=True)
    vendor_id: str | None = "UNASSIGNED"
    booth_number: int = Field(primary_key=True)

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Conventiondb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Conventiondb connection closed.")


def retrieve_booth(conv_id: str | None, vendor_id: str | None):
    with Session(engine) as session:
        if vendor_id and conv_id:
            statement = select(VendorBooths).where(
                VendorBooths.vendor_id == vendor_id and VendorBooths.conv_id == conv_id)
        elif vendor_id:
            statement = select(VendorBooths).where(
                VendorBooths.vendor_id == vendor_id)
        elif conv_id:
            statement = select(VendorBooths).where(
                VendorBooths.conv_id == conv_id)
        else:
            return None
        booths = session.exec(statement).all()
        return list(map(lambda b: BoothAssignmentResp(conv_id=b.conv_id, vendor_id=b.vendor_id, booth_number=b.booth_number), booths))


def create_booth(conv_id, booth_number):
    with Session(engine) as session, session.begin():
        new_assignment = VendorBooths(
            conv_id=conv_id, booth_number=booth_number)
        session.add(new_assignment)
        session.commit()


def assign_booth(conv_id, booth_number, vendor_id):
    with Session(engine) as session, session.begin():
        statement = update(VendorBooths).where(
            and_(VendorBooths.conv_id == conv_id, VendorBooths.booth_number == booth_number)).values(vendor_id=vendor_id)
        result = session.exec(statement)
        session.commit()
        return result.rowcount


def unassign_booth(conv_id, booth_number):
    with Session(engine) as session, session.begin():
        statement = update(VendorBooths).where(and_(VendorBooths.conv_id == conv_id,
                                                    VendorBooths.booth_number == booth_number)).values(vendor_id=None)
        result = session.exec(statement)
        session.commit()
        return result.rowcount


def remove_booth(conv_id, booth_number):
    with Session(engine) as session, session.begin():
        statement = select(VendorBooths).where(
            VendorBooths.conv_id == conv_id and VendorBooths.booth_number == booth_number)
        target_booth = session.exec(statement).first()
        session.delete(target_booth)
        session.commit()
