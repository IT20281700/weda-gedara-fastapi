from Imports.Imports import *

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from Security.AuthService import authenticate_user, create_access_token
from config.db import db
from models.TokenModel import Token

ACCESS_TOKEN_EXPIRATION_MINUTES = int(env['ACCESS_TOKEN_EXPIRATION_MINUTES'])

router = APIRouter(
    prefix=f"{env['BASE_URL']}",
    tags=['authentication']
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}