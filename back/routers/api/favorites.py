from fastapi import APIRouter, Depends, Path, HTTPException, Query
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.limit_offset import LimitOffsetParams, LimitOffsetPage
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import Response

from controllers.users import current_active_user
from routers.api.shemas import PostCreateScheme, PostUpdateScheme, PostPatchScheme, PostReadScheme, PostShortScheme, \
    FavoriteScheme, FavoritesScheme
from db.engine import get_async_session
from db.models import FavouriteUser, Post, User, Comment

router = APIRouter()


@router.get('/users/{user_id}/favorites/',
            response_model=LimitOffsetPage[FavoriteScheme])
async def get_user_favorite(user_id: int,
                            limit: int = Query(default=50, lt=101, gt=0),
                            offset: int = Query(default=0, gt=-1),
                            user: User = Depends(current_active_user),
                            session: AsyncSession = Depends(get_async_session)):
    author = await session.get(User, user_id)

    if author is None:
        return HTTPException(status_code=404, detail='user not found')

    if author.is_closed and not user.is_superuser:
        return HTTPException(status_code=403, detail='Access denied')

    params = LimitOffsetParams(limit=limit, offset=offset)

    request = select(FavouriteUser).where(FavouriteUser.user_id == user_id)

    return await paginate(
        session,
        request,
        params=params
    )


@router.post('/users/{user_id}/favorites/{fav_id}',
             name='добавляет любомого пользователя')
async def post_user_favorite(user_id: int,
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

    if fav_user is not None:
        raise HTTPException(status_code=400, detail='favorite user already exist')

    favorite = FavouriteUser()
    favorite.user_id = user_id
    favorite.favourite_user_id = fav_id

    session.add(favorite)
    await session.commit()
    await session.refresh(favorite)
    return FavoriteScheme.from_orm(favorite)


@router.delete('/users/{user_id}/favorites/{fav_id}',
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
