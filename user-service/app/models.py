from typing import Literal

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    user_type: Literal["vendor", "attendee"]


class UserUpdate(BaseModel):
    id: str
    username: str | None = None
    user_type: Literal["vendor", "attendee"] | None = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    user_type: Literal["vendor", "attendee"]
