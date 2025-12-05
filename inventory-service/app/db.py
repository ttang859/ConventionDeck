import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, update

from .models import InventoryCreate, InventoryResponse

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


class VendorInventory(SQLModel, table=True):
    __tablename__ = "vendor_inventory"  # type: ignore # matches our table name in SQL

    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    card_name: str  # EmailStr
    owner_id: str
    price: float  # Literal["vendor", "attendee"]

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Inventorydb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Inventorydb connection closed.")
