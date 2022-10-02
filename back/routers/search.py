from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import parse_obj_as
from sqlalchemy import or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from controllers.users import current_active_user
from db.engine import get_async_session
from db.models import Post, User
from routers.shemas import GetSearchObjs, ShortObj

router = APIRouter()


@router.get('/search/')
async def search(q: str = Query(title='search string', min_length=5, max_length=30),
                 current_user: User = Depends(current_active_user),
                 session: AsyncSession = Depends(get_async_session)) -> GetSearchObjs:

    if current_user.is_superuser:
        req = select(User).where(or_(
            User.username.ilike(f'%{q}%'),
            User.email.ilike(f'%{q}%'),
        )).limit(20)
    else:
        req = select(User).where(User.is_closed.is_(False), or_(
            User.username.ilike(f'%{q}%'),
            User.email.ilike(f'%{q}%'),
        )).limit(20)
    items = []
    users = (await session.execute(req)).scalars().all()

    if users:
        items.extend(parse_obj_as(List[ShortObj], users))

    if current_user.is_superuser:
        req = select(Post).where(or_(
            Post.title.ilike(f'%{q}%'),
            Post.content.ilike(f'%{q}%'),
        )).order_by(desc(Post.created_at)).limit(20)
    else:
        req = select(Post).where(Post.is_closed.is_(False), or_(
            Post.title.ilike(f'%{q}%'),
            Post.content.ilike(f'%{q}%'),
        )).order_by(desc(Post.created_at)).limit(20)

    posts = (await session.execute(req)).scalars().all()
    if posts:
        items.extend(parse_obj_as(List[ShortObj], posts))
    return GetSearchObjs(count=len(items), items=items)
