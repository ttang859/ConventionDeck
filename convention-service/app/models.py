from datetime import datetime

from pydantic import BaseModel, field_validator


class ConventionCreate(BaseModel):
    convention_name: str
    host_id: str
    start: datetime
    loc: str
    vendor_count: int = 0

    # @field_validator("start")
    # @classmethod
    # def validate_date(cls, value):
    #     try:
    #         format_str="%Y-%m-%d %H:%M:%S"
    #         datetime.strptime(value, format_str)
    #     except Exception as e:
    #         raise e


class ConventionResponse(BaseModel):
    id: str
    convention_name: str
    host_id: str
    start: datetime
    loc: str
    vendor_count: int

class ConventionRetrieve(BaseModel):
    conv_id: str | None = None
    host_id: str | None = None

class ConventionUpdate(BaseModel):
    id: str
    start: str | None = None
    loc: str | None = None
    vendor_count: int | None = None

class ConventionDelete(BaseModel):
    id: str
