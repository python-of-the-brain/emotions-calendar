from fastapi.exceptions import HTTPException
from loguru import logger 
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse


class ErrorResult(BaseModel):
    code: int
    message: str


def http_exception_handler(request: Request,  exc: HTTPException):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResult(code=exc.status_code, message=exc.detail).dict()
    )