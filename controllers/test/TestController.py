from fastapi import APIRouter, Depends, status
from Security.AuthService import oauth_2_schema
from os import environ as env

# logger
from Imports.logger import getLogger
log = getLogger(__name__)

router = APIRouter(
    prefix=f"{env['BASE_URL']}" + '/test',
    tags=['test'],
    dependencies=[Depends(oauth_2_schema)]
)


@router.get("/", response_model=str, status_code=status.HTTP_200_OK)
async def test():
    log.info('test method called')
    return 'Hello'
