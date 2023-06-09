from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "381668887f8042aeb59309e3fb697fc4289deaf1e7ea2c1194810e6e2b982689"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

fake_db = {
    "tim": {
        "userId": 1,
        "email": "tim@gmail.com",
        "full_name": "Tim Ruscica",
        "hashed_password": "",
        "disabled": False
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str or None = None

class User(BaseModel):
    userId: int
    email: str or None = None
    full_name: str or None = None
    disabled: bool

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], depreacted="auto")
oauth_2_schema = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

