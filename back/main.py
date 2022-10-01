from fastapi import FastAPI, HTTPException
import uvicorn

from config import get_settings
from errors import http_exception_handler

from routers.users import router as user_router


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

    application.include_router(router=user_router, prefix='/users')

    return application


app = get_application()



if __name__ == '__main__':
    app = get_application()
    uvicorn.run(app, host='127.0.0.1', port=8000)