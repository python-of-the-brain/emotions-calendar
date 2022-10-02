import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from controllers.users import current_active_user
from db.engine import get_async_session
from db.models import User, Status, Post, CalendarDay, Comment
from routers.api.shemas import StatusScheme, ProfileScheme, PostReadScheme, CurrentStatusScheme, \
    CalendarDayScheme, UserReadForComment

router = APIRouter(tags=['Профиль'])


@router.get('/user/{user_id}/profile/',
            name='Возвращает полный профиль пользователя', response_model=ProfileScheme)
async def get_user_posts(
        user_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    if author.is_closed and not user.is_superuser:
        return HTTPException(status_code=403, detail='Access denied')

    query = select(Post).where(Post.user_id == user_id).limit(20).options(
        selectinload(Post.comments),
        selectinload(Post.emotion),
        selectinload(Post.comments, Comment.emotion),
        selectinload(Post.comments, Comment.user),
    )

    posts = (await session.execute(query)).scalars().all()

    query = select(Status).where(Status.user_id == user_id).limit(10).order_by(
            desc(Status.created_at))

    status = (await session.execute(query)).scalars().all()

    today = datetime.date.today()
    first_day_month = datetime.date(year=today.year, month=today.month, day=1)

    query = select(CalendarDay).where(CalendarDay.day <= today, CalendarDay.day >= first_day_month)

    days = (await session.execute(query)).scalars().all()

    current_status = None if not len(status) else status[0]

    data = {
        'user': UserReadForComment.from_orm(author),
        'posts': parse_obj_as(List[PostReadScheme], posts),
        'current_status': CurrentStatusScheme.from_orm(current_status),
        'previous_statuses': parse_obj_as(List[StatusScheme], status[1:]),
        'calendar_days': parse_obj_as(List[CalendarDayScheme], days)
    }

    return ProfileScheme(**data)
