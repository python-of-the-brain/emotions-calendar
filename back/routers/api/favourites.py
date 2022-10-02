from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.limit_offset import LimitOffsetParams, LimitOffsetPage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import Response

from controllers.users import current_active_user
from db.engine import get_async_session
from db.models import FavouriteUser, User
from routers.api.shemas import FavouriteInputScheme, FavouriteOutputScheme

favourite_router = APIRouter(tags=['Избранное'])


@favourite_router.get('/users/{user_id}/favourites/',
                      response_model=LimitOffsetPage[FavouriteOutputScheme],
                      name='Возвращает список избранных пользователей')
async def get_list_favourite_user(user_id: int,
                                  limit: int = Query(default=50, lt=101, gt=0),
                                  offset: int = Query(default=0, gt=-1),
                                  current_user: User = Depends(current_active_user),
                                  session: AsyncSession = Depends(get_async_session)):
    target_user = await session.get(User, user_id)

    if target_user is None:
        return HTTPException(status_code=404, detail='Target user is not found')

    if target_user.is_closed and not current_user.is_superuser and user_id != current_user.id:
        return HTTPException(status_code=403, detail='Access denied')

    params = LimitOffsetParams(limit=limit, offset=offset)
    request = select(FavouriteUser).where(FavouriteUser.user_id == user_id)
    return await paginate(session, request, params=params)


@favourite_router.post('/users/{user_id}/favourites/',
                       name='добавляет любимого пользователя',
                       response_model=FavouriteOutputScheme)
async def add_favourite_user(user_id: int,
                             favourite_user_data: FavouriteInputScheme,
                             current_user: User = Depends(current_active_user),
                             session: AsyncSession = Depends(get_async_session)):
    target_user = await session.get(User, user_id)
    favourite_user_id = favourite_user_data.favourite_user_id

    if target_user is None:
        return HTTPException(status_code=404, detail='User not found')

    favourite_user = await session.get(User, favourite_user_id)

    if favourite_user is None:
        return HTTPException(status_code=404, detail='Favourite user is not found!')

    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{current_user.username} is\'t superuser')

    query = select(FavouriteUser).where(FavouriteUser.user_id == user_id,
                                        FavouriteUser.favourite_user_id == favourite_user.id)
    fav_user = (await session.execute(query)).scalars().first()

    if fav_user is not None:
        raise HTTPException(status_code=400, detail='favorite user already exist')

    favorite = FavouriteUser(favourite_user_id=favourite_user_id, user_id=user_id)

    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return FavouriteOutputScheme.from_orm(favorite)


@favourite_router.delete('/users/{user_id}/favourites/{fav_id}',
                         name='удаляет любимого пользователя')
async def delete_favorite(user_id: int,
                          fav_id: int,
                          user: User = Depends(current_active_user),
                          session: AsyncSession = Depends(get_async_session)):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    author = await session.get(User, fav_id)

    if author is None:
        return HTTPException(status_code=404, detail='favorite user not found')

    if user.id != user_id and not user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{user.username} is\'t superuser or post author')

    query = select(FavouriteUser).where(FavouriteUser.user_id == user_id,
                                        FavouriteUser.favourite_user_id == fav_id)
    fav_user = (await session.execute(query)).scalars().first()

    if fav_user is None:
        raise HTTPException(status_code=404, detail='fav not found')

    await session.delete(fav_user)
    await session.commit()
    return Response(status_code=204)
