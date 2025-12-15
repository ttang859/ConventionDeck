
from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class BoothAssignmentResp(BaseModel):
    conv_id: str
    vendor_id: str | None
    booth_number: int


class ValidAssignment(BaseModel):
    conv_id: str
    vendor_id: str | None = "UNASSIGNED"
    booth_number: int


class AllBooths(BaseModel):
    conv_id: str
    total_booths: int

    @field_validator("total_booths")
    @classmethod
    def validate_total_booths(cls, value):
        if value <= 0:
            raise HTTPException(
                400, "Total amount of Booths has to be positive, non-zero value")
        return value


class GetBoothOptions(BaseModel):
    conv_id: str | None = None
    vendor_id: str | None = None
