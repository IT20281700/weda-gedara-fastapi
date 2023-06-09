from Imports.Imports import *
from controllers.authentication import AuthenticationController
from controllers.test import TestController
from controllers.user import UserController
from models.error.ErrorModel import BadAlertException

app = FastAPI(
    docs_url=env['BASE_URL'] + "/docs",
    redoc_url=None,
    title="Weda Gedara FastAPI",
    description="New world apis from chamodex::",
    version="1.0",
    openapi_url=env['BASE_URL'] + "/openapi.json",
    responses={
        400: {"model": ErrorDto},
        401: {"model": ErrorDto}
    },
)


@app.get("/", tags=['base'], deprecated=True)
async def _root():
    return "server_is_up_and_running"


@app.get(env['BASE_URL'], tags=['base'], deprecated=True)
async def root():
    return {"message": "Arogya Paramalaba!!!"}


# include all controller routers
app.include_router(AuthenticationController.router)  # authentication router
app.include_router(UserController.router)  # user router
app.include_router(TestController.router)  # user router


# global error handler
@app.exception_handler(BadAlertException)
async def unicorn_exception_handler(request: Request, exc: BadAlertException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status_code": f"{status.HTTP_400_BAD_REQUEST}",
            "path": f"{request.scope.get('path')}",
            "message": f"{exc.description}"
        }
    )


# global error handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": f"{exc.status_code}",
            "path": f"{request.scope.get('path')}",
            "message": f"{exc.detail}"
        }
    )
