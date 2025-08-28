from typing import Optional
from pydantic import BaseModel, field_validator

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None   # allows null/False
    phone: Optional[str] = None   # allows null/False

    @field_validator("email", "phone", mode="before")
    def falsy_to_none(cls, v):
        if v is False:
            return None
        return v