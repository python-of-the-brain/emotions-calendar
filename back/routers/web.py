from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from controllers.jinja import templates

web_router = APIRouter(default_response_class=HTMLResponse, prefix='/web', include_in_schema=False)


@web_router.get('/')
async def index_route(request: Request):
    context = {
        'request': request,
        'index_url': request.app.url_path_for('index_route'),
        'search_url': request.app.url_path_for('search_route'),
        'login_url': request.app.url_path_for('login_route'),
        'register_url': request.app.url_path_for('register_route'),
    }
    return templates.TemplateResponse("index.html", context=context)


@web_router.get('/login', response_class=HTMLResponse)
async def login_route(request: Request):
    context = {
        'request': request,
        'index_url': request.app.url_path_for('index_route'),
        'search_url': request.app.url_path_for('search_route'),
        'login_url': request.app.url_path_for('login_route'),
        'register_url': request.app.url_path_for('register_route'),
    }
    return templates.TemplateResponse("login.html", context=context)


@web_router.get('/register', response_class=HTMLResponse)
async def register_route(request: Request):
    context = {
        'request': request,
        'index_url': request.app.url_path_for('index_route'),
        'search_url': request.app.url_path_for('search_route'),
        'login_url': request.app.url_path_for('login_route'),
        'register_url': request.app.url_path_for('register_route'),
    }
    return templates.TemplateResponse('register.html', context=context)


@web_router.get('/search', response_class=HTMLResponse)
async def search_route(request: Request):
    return templates.TemplateResponse('search.html', context={'request': request})


@web_router.get('/profile/{user_id}', response_class=HTMLResponse)
async def profile_route(request: Request):
    return templates.TemplateResponse('profile.html', context={'request': request})