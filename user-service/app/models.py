from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    username: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
