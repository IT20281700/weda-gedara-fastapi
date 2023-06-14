from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError
import jwt
from passlib.context import CryptContext
from config.db import get_connection
from models.TokenModel import TokenData
from models.UserModel import UserInDB
from Imports.Imports import SECRET_KEY, ALGORITHM
from pymongo.collection import Collection
from useEnum.Enum import SchemasEnum
from fastapi.exceptions import RequestValidationError

# logger
from Imports.logger import getLogger
log = getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_schema = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Collection, email: str):
    user_data = db.find_one({"email": email})
    if user_data:
        return UserInDB(**user_data)


def authenticate_user(db: Collection, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        db = get_connection().get_collection(SchemasEnum.USER.value)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM], options={"verify_signature": False})
        email: str = payload.get('sub')
        if email is None:
            raise credential_exception

        token_data = TokenData(email=email)
        user = get_user(db, email=token_data.email)
        if user is None:
            raise credential_exception

        return user
    except ExpiredSignatureError as e:
        log.error(e)
        log.error("Token expired")
        raise HTTPException(status_code=401, detail="Token expired.", headers={
                            "WWW-Authenticate": "Bearer"})
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=401, detail=f"{e.errors()}", headers={
                                "WWW-Authenticate": "Bearer"})
        else:
            log.error(e)
            raise credential_exception


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
