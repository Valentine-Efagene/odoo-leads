from pydantic import BaseModel, Field

class AuthDto(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username" : "User Odoo username",
                "password" : "User password"
            }
        },
        'arbitrary_types_allowed': True,
    }