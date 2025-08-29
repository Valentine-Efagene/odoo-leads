from dataclasses import dataclass
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional, Annotated
from pydantic import BaseModel, EmailStr, StringConstraints


class Lead(BaseModel):
    email: EmailStr
    phone: Annotated[
        str, StringConstraints(pattern=r"^\+?\d{1,4}-\d+$")
    ]  # e.g. +234-8012345678

    # optional fields
    name: Optional[str] = None
    utm: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    property_type: Optional[str] = None
    payment_option: Optional[str] = None
    place_of_work: Optional[str] = None
    salary_range: Optional[str] = None
    project_location: Optional[str] = None


def responseModel(data, message, code: int = 200):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    data: T
    message: str
    code: int = 200
