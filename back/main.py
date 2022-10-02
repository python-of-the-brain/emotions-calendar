import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from config import get_settings
from controllers.users import fastapi_users, auth_backend
from errors import http_exception_handler
from routers import external_api_router
from routers.api.comments import router as comment_router
from routers.api.favourites import favourite_router
from routers.api.post import router as post_router
from routers.api.profile import router as profile_router
from routers.api.search import router as search_router
from routers.api.shemas import UserRead, UserCreate, UserUpdate
from routers.api.status import router as status_router
from routers.web import web_router


def include_routers(app: FastAPI) -> None:
    api = APIRouter(prefix='/api')
    api_routers = [external_api_router,
                   post_router, comment_router, search_router,
                   status_router, profile_router, favourite_router]
    for router in api_routers:
        api.include_router(router)
    app.include_router(api)
    app.include_router(web_router)


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

    application.mount("/static", StaticFiles(directory="frontend/static"), name="static")

    application.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
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

    include_routers(app=application)
    add_pagination(application)
    return application


app = get_application()

if __name__ == '__main__':
    app = get_application()
    uvicorn.run(app, host='127.0.0.1', port=8000)
