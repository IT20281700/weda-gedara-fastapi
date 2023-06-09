# from fastapi import FastAPI, Depends, HTTPException, status, APIRouter

# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import JSONResponse, PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from Security.AuthService import oauth_2_schema
# from config.db import get_connection
# from models.response.CreateResponseModel import CreateResponseModel

# from models.error.ErrorModel import ErrorDto

from os import environ as env

SECRET_KEY = env['SECRET_KEY']
ALGORITHM = env['ALGORITHM']
