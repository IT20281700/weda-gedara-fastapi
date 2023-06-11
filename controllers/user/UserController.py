from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from Security.AuthService import get_current_active_user, oauth_2_schema
from config.db import get_connection
from models.UserModel import User
from os import environ as env
from useEnum.Enum import SchemasEnum
from models.response.ResponseTemplateModes import userEntity, userListEntity


# logger
from Imports.logger import getLogger
log = getLogger(__name__)

router = APIRouter(
    prefix=f"{env['BASE_URL']}"+'/users',
    tags=['user'],
    dependencies=[Depends(oauth_2_schema), Depends(get_current_active_user)]
)


@router.get("/me/", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    log.info('read_users_me method called')
    return current_user


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def read_all_users():
    log.info('read_all_users method called')
    try:
        db = get_connection().get_collection(SchemasEnum.USER.value)
        return userListEntity(db.find())
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
