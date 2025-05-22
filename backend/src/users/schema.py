from datetime import datetime

from pydantic import BaseModel, field_validator
import re


class UserIn(BaseModel):
    email: str
    first_id: str
    last_name: str
    passwrod: str
    is_admin: bool

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise ValueError("Provided email is not valid")
        return value


class UserOut(BaseModel):
    id: int
    email: str
    first_id: str
    last_name: str
    passwrod: str
    is_admin: bool
    created_at: datetime
