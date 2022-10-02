from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from controllers.jinja import templates

login_web_router = APIRouter()


@login_web_router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html")
