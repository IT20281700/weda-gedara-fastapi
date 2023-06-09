from Imports.Imports import *
from Security.AuthService import get_current_active_user
from models.UserModel import User

router = APIRouter(
    prefix=f"{env['BASE_URL']}"+'/users',
    tags=['user'],
    dependencies=[Depends(oauth_2_schema)]
)


@router.get("/me/", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
