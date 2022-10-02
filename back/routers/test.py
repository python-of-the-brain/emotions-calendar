from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from controllers.jinja import templates

from db.engine import get_async_session
from db.models import User


router = APIRouter()


@router.get("/test/user_name/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int, session: AsyncSession = Depends(get_async_session)):
    data = {
        'username': (await session.get(User, id)).username,
        'id': id,
        'request': request
    }

    return templates.TemplateResponse("item.html", context=data)
