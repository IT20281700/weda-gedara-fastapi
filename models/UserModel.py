from pydantic import BaseModel


class User(BaseModel):
    userId: int
    email: str or None = None
    full_name: str or None = None
    disabled: bool

class UserInDB(User):
    hashed_password: str
