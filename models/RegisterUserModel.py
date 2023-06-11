from dataclasses import Field
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel


class RegisterUserDto(BaseModel):
    user_id: int | None = None
    user_type: str
    first_name: str
    last_name: str
    gender: str
    email: str
    mobile: str
    hashed_password: str
    address: str
    addr_no: str
    zip_code: int
    state: str | None = None
    city: str
    disabled: bool | None = None
