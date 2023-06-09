from fastapi import FastAPI, Depends, HTTPException, status
from os import environ as env
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = env['SECRET_KEY']
ALGORITHM = env['ALGORITHM']
ACCESS_TOKEN_EXPIRATION_MINUTES = int(env['ACCESS_TOKEN_EXPIRATION_MINUTES'])

db = {
    "chamod@gmail.com": {
        "userId": 1,
        "email": "chamod@gmail.com",
        "full_name": "Chamod Ishankha",
        "hashed_password": "$2b$12$alDi8k3BWacU6sRYQTY4i.7WN.6mKlbv4oqWQqHHfAw7a4Hg8FDRS",
        "disabled": False
    },
    "chamod1@gmail.com": {
        "userId": 2,
        "email": "chamod1@gmail.com",
        "full_name": "Chamod Ishankha",
        "hashed_password": "$2b$12$alDi8k3BWacU6sRYQTY4i.7WN.6mKlbv4oqWQqHHfAw7a4Hg8FDRS",
        "disabled": False
    },
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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_schema = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# base url path
base_url = "/api/v1/weda-gedara"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, email: str):
    if email in db:
        user_data = db[email]
        return UserInDB(**user_data)


def authenticate_user(db, email: str, password: str):
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
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credential_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception

    user = get_user(db, email=token_data.email)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@app.post(base_url+"/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get(base_url+"/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user