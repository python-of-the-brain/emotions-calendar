from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from config import get_settings
from routers import external_api_router
from controllers.users import fastapi_users, auth_backend
from errors import http_exception_handler


def include_routers(app: FastAPI):
    routers = [external_api_router]
    for router in routers:
        app.include_router(router)
from routers.shemas import UserRead, UserCreate, UserUpdate
from routers.test import router as test_router
from routers.post import router as post_router
from routers.comments import router as comment_router
from routers.search import router as search_router
from routers.status import router as status_router
from routers.profile import router as profile_router


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
    application.include_router(router=comment_router)
    application.include_router(router=search_router)
    application.include_router(router=status_router)
    application.include_router(router=profile_router)

    add_pagination(application)
    include_routers(app=application)

    return application


app = get_application()


if __name__ == '__main__':
    app = get_application()
    uvicorn.run(app, host='127.0.0.1', port=8000)
