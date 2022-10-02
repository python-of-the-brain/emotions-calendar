from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import Response

from controllers.users import current_active_user
from db.engine import get_async_session
from db.models import User, Status, Emotion
from routers.shemas import StatusScheme

router = APIRouter(tags=['Статусы'])


@router.get('/users/{user_id}/current_status/')
async def set_status(user_id: int,
                     user: User = Depends(current_active_user),
                     session: AsyncSession = Depends(get_async_session)
                     ):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    if author.is_closed and not user.is_superuser:
        return HTTPException(status_code=403, detail='Access denied')

    query = select(Status).where(Status.user_id == user_id).order_by(desc(Status.created_at))

    status = (await session.execute(query)).scalars().first()

    if status is None:
        return HTTPException(status_code=404, detail='status not found')

    return StatusScheme.from_orm(status)


@router.post('/users/{user_id}/status/')
async def update_status(user_id: int,
                        status_data: StatusScheme,
                        user: User = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)
                        ):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    if user.id != user_id and not user.is_superuser:
        return HTTPException(status_code=403, detail='Access denied')

    emotion = await session.get(Emotion, status_data.dict()['emotion_id'])

    if emotion is None:
        return HTTPException(status_code=404, detail='emotion not found')

    status = Status(**status_data.dict(), user_id=user_id)
    session.add(status)
    await session.commit()
    await session.refresh(status)
    return StatusScheme.from_orm(status)


@router.delete('/users/{user_id}/current_status/')
async def delete_status(user_id: int,
                        user: User = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    if user.id != user_id and not user.is_superuser:
        return HTTPException(status_code=403, detail='Access denied')

    query = select(Status).where(Status.user_id == user_id).order_by(desc(Status.created_at))

    status = (await session.execute(query)).scalars().first()

    if status is None:
        return HTTPException(status_code=404, detail='status not found')

    await session.delete(status)
    await session.commit()
    return Response(status_code=204)
