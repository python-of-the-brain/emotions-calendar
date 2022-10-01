import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from config import get_settings
from controllers.users import fastapi_users, auth_backend
from errors import http_exception_handler
from routers.shemas import UserRead, UserCreate, UserUpdate
from routers.users import router as user_router
from routers.test import router as test_router
from routers.post import router as post_router


def get_application() -> FastAPI:
    """AppFactory"""

    settings = get_settings()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        description='Тот самый хакатон',
    )
    application.add_exception_handler(HTTPException, http_exception_handler)

    application.mount("/static", StaticFiles(directory="static"), name="static")

    application.include_router(router=user_router, prefix='/users')
    application.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["registration"],
    )
    application.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    # TODO email verification
    # application.include_router(
    #     fastapi_users.get_verify_router(UserRead),
    #     prefix="/auth",
    #     tags=["auth"],
    # )
    application.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )

    application.include_router(router=test_router)
    application.include_router(router=post_router)

    return application


app = get_application()


if __name__ == '__main__':
    app = get_application()
    uvicorn.run(app, host='127.0.0.1', port=8000)