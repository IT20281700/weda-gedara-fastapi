from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from datetime import timedelta
from Security.AuthService import authenticate_user, create_access_token, get_password_hash
from config.db import get_connection
from models.RegisterUserModel import RegisterUserDto
from models.TokenModel import Token
from os import environ as env
from models.response.CreateResponseModel import CreateResponseModel
from useEnum.Enum import SchemasEnum, SchemaSequencesEnum
from utils.common.SequenceGenerator import get_next_sequence_value

# logger
from Imports.logger import getLogger
log = getLogger(__name__)

ACCESS_TOKEN_EXPIRATION_MINUTES = int(env['ACCESS_TOKEN_EXPIRATION_MINUTES'])

router = APIRouter(
    prefix=f"{env['BASE_URL']}"+"/auth",
    tags=['authentication']
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    log.info("login_for_access_token method called:")
    # get db connection
    db = get_connection()
    user = authenticate_user(
        db[SchemasEnum.USER.value], form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_app_user(user: RegisterUserDto):
    log.info("register_app_user method called:")
    # get db connection
    db = get_connection()
    try:
        # generate sequence and insert to dto
        user.user_id = get_next_sequence_value(
            SchemasEnum.SEQUENCES.value, SchemaSequencesEnum.USER.value, db)

        # process password hash
        # set hash as password
        user.hashed_password = get_password_hash(user.hashed_password)

        # set disabled False
        user.disabled = False

        # save
        result = db[SchemasEnum.USER.value].insert_one(dict(user))
        return CreateResponseModel(id=str(result.inserted_id), status="success", desc="User registration successful")
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
