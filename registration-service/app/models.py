from pydantic import BaseModel

class RegisteredPair(BaseModel):
    conv_id: str
    attendee_id:str
