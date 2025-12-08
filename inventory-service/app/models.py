from pydantic import BaseModel, field_validator


class InventoryCreate(BaseModel):
    card_name: str
    owner_id: str
    price: float

    @field_validator("price")
    @classmethod
    def check_price(cls, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        return round(value, ndigits=2)


class InventoryRetrieve(BaseModel):
    owner_id: str | None


class InventoryUpdate(BaseModel):
    id: str
    # owner_id: str
    price: float | None = None


class InventoryDelete(BaseModel):
    id: str


class InventoryResponse(BaseModel):
    id: str
    card_name: str
    owner_id: str
    price: float
