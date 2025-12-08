import os
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select, update, delete

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
    card_name: str
    owner_id: str
    price: float

# create tables if they don't exist


def init_db():
    SQLModel.metadata.create_all(engine)
    print("Inventorydb initialized and tables created (if not exist).")

# close the database connection cleanly


def close_db_connection():
    engine.dispose()
    print("Inventorydb connection closed.")


def create_card_entry(card_name, owner_id, price):
    with Session(engine) as session, session.begin():
        inv_entry = VendorInventory(
            card_name=card_name, owner_id=owner_id, price=price)
        session.add(inv_entry)
        session.commit()


def get_card_entries(owner_id):
    with Session(engine) as session:
        if owner_id:
            statement = select(VendorInventory).where(
                VendorInventory.owner_id == owner_id)
        else:
            statement = select(VendorInventory)
        card_entries = session.exec(statement).all()
        return list(map(lambda c: InventoryResponse(id=c.id, card_name=c.card_name, owner_id=c.owner_id, price=c.price).model_dump(), card_entries))

def update_card_entry(card_id, price):
    with Session(engine) as session, session.begin():
        value_hash = {}
        if price:
            value_hash["price"] = price
        statement = update(VendorInventory).where(VendorInventory.id == card_id).values(value_hash)
        session.exec(statement)
        session.commit()

def delete_card_entry(card_id):
    with Session(engine) as session, session.begin():
        statement = select(VendorInventory).where(
            VendorInventory.id == card_id)
        if session.exec(statement).one_or_none():
            statement = delete(VendorInventory).where(
                VendorInventory.id == card_id)
            session.exec(statement)
            session.commit()
            return True
        else:
            return False
