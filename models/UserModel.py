import datetime
from pydantic import BaseModel


class User(BaseModel):
    user_id: int | None = None
    user_type: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: datetime.date | None = None
    age: int | None = None
    gender: str | None = None
    email: str
    mobile: str | None = None
    address: str | None = None
    addr_no: str | None = None
    zip_code: int | None = None
    state: str | None = None
    city: str | None = None
    disabled: bool | None = None
    last_login: datetime.datetime | None = None
    login_time: datetime.datetime | None = None


class UserInDB(User):
    hashed_password: str


class LoginRequest(BaseModel):
    username: str
    password: str
