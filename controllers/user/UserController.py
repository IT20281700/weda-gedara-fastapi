import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from Security.AuthService import get_current_active_user, oauth_2_schema
from config.db import get_connection
from models.UserModel import User
from os import environ as env
from models.error.ErrorModel import BadAlertException
from useEnum.Enum import SchemasEnum
from models.response.ResponseTemplateModes import userEntity, userListEntity
import utils.common.Common as common


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
    current_user.age = common.get_age_from_birth_date(current_user.birth_date)
    return current_user


@router.get("/", response_model=list[User], status_code=status.HTTP_200_OK)
async def read_all_users():
    log.info('read_all_users method called')
    try:
        db = get_connection().get_collection(SchemasEnum.USER.value)

        user_list: list[User] = userListEntity(db.find())

        for user in user_list:
            us: User = User(**user)
            birth_date: datetime.date = us.birth_date
            user['age'] = common.get_age_from_birth_date(birth_date)

        return user_list
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")


@router.put('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int, user: User):
    log.info('update_user_by_id method called')
    try:
        db = get_connection().get_collection(SchemasEnum.USER.value)

        user_doc = db.find_one({'user_id': user_id})

        # validate
        if (user.first_name == '' or user.first_name == 'null'):
            raise BadAlertException('First name is required')
        if (user.last_name == '' or user.last_name == 'null'):
            raise BadAlertException('Last name is required')
        if (user.addr_no == '' or user.addr_no == 'null'):
            raise BadAlertException('House number is required')
        if (user.address == '' or user.address == 'null'):
            raise BadAlertException('Address is required')
        if (user.state == '' or user.state == 'null'):
            raise BadAlertException('State is required')
        if (user.city == '' or user.city == 'null'):
            raise BadAlertException('City is required')
        if (user.zip_code == 0):
            raise BadAlertException('Zip code is required')
        if (user.user_id != user_id):
            raise BadAlertException('User id not match')
        if (user_doc) is None:
            raise BadAlertException('User not found by id: '+str(user_id))

        userDoc: User = User(**user_doc)
        # set updated values
        userDoc.first_name = user.first_name
        userDoc.last_name = user.last_name
        userDoc.addr_no = user.addr_no
        userDoc.address = user.address
        userDoc.state = user.state
        userDoc.city = user.city
        userDoc.zip_code = user.zip_code

        user_dict = userDoc.dict()

        # convert date
        user_dict['birth_date'] = user_dict['birth_date'].isoformat()

        # remove non database fields
        user_dict.pop('age')

        # update doc
        userDoc = db.find_one_and_update(
            {'user_id': user_id}, {'$set': user_dict})

        return User(**user_dict)
    except Exception as e:
        if isinstance(e, RequestValidationError):
            log.error(e.errors())
            raise HTTPException(status_code=400, detail=f"{e.errors()}")
        else:
            log.error(e)
            raise HTTPException(status_code=400, detail=f"{e}")
