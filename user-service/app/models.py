from typing import Literal
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    username: str
    user_type: Literal["vendor", "attendee"]

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    user_type: Literal["vendor", "attendee"]
