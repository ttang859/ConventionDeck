from pydantic import BaseModel, field_validator


class InventoryCreate(BaseModel):
    card_name: str
    owner_id: str
    price: float

    @field_validator("price")
    @classmethod
    def check_price(cls,value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value

class InventoryUpdate(BaseModel):
    id: str
    owner_id: str
    price: float|None = None

class InventoryResponse(BaseModel):
    id: str
    card_name: str
    owner_id: str
    price: float
