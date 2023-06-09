from Imports.Imports import *

router = APIRouter(
    prefix=f"{env['BASE_URL']}" + '/test',
    tags=['test'],
    dependencies=[Depends(oauth_2_schema)]
)


@router.get("/", response_model=str, status_code=status.HTTP_200_OK)
async def test():
    return 'Hello'
