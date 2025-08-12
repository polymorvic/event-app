from datetime import datetime

from pydantic import BaseModel, field_validator
import re


class UserIn(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool | None = False

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str | ValueError:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Provided email is not valid")
        return value


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool
    created_at: datetime
    is_activated: bool = False
