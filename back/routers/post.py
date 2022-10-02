from fastapi import APIRouter, Depends, Path, HTTPException, Query
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.limit_offset import LimitOffsetParams, LimitOffsetPage
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import Response

from controllers.users import current_active_user
from routers.shemas import PostCreateScheme, PostUpdateScheme, PostPatchScheme, PostReadScheme, PostShortScheme
from db.engine import get_async_session
from db.models import Post, User, Comment

router = APIRouter()


@router.get('/user/{user_id}/posts/{post_id}',
            response_model=PostReadScheme,
            name='возвращает post пользователя по id')
async def get_user_post(user_id: int, post_id: int, current_user: User = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)
                        ):
    author = await session.get(User, user_id)

    if author is None:
        raise HTTPException(status_code=404, detail='user not found')

    is_closed = (await session.execute(select(Post.is_closed).where(Post.id == post_id))).scalars().first()

    if is_closed is None:
        raise HTTPException(status_code=404, detail=f'Post not found')

    if current_user.id != user_id and not current_user.is_superuser and is_closed:
        raise HTTPException(status_code=403, detail=f'{current_user.username} is\'t superuser or post author')
    post = (await session.get(Post, post_id, options=(
        selectinload(Post.comments),
        selectinload(Post.emotion),
        selectinload(Post.comments, Comment.emotion),
        selectinload(Post.comments, Comment.user),
    )))

    if post is None:
        raise HTTPException(status_code=404, detail=f'{current_user.username} have no post with id {post_id}')
    return PostReadScheme.from_orm(post)


@router.get('/user/{user_id}/posts',
            response_model=LimitOffsetPage[PostShortScheme],
            name='возвращает posts пользователя')
async def get_user_posts(
        user_id: int,
        limit: int = Query(default=50, lt=101, gt=0),
        offset: int = Query(default=0, gt=-1),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    post_author = (await session.execute(select(User).where(User.id == user_id))).scalars().first()

    if post_author is None:
        raise HTTPException(status_code=404, detail=f'Posts not found')

    if user_id != user.id and post_author.is_closed and not user.is_superuser:
        raise HTTPException(status_code=403, detail='Access denied')

    params = LimitOffsetParams(limit=limit, offset=offset)

    if user.is_superuser:
        request = select(Post).where(Post.user_id == user_id).order_by(
            desc(Post.created_at))
    else:
        request = select(Post).where(Post.user_id == user_id,
                                     Post.is_closed.is_(False)).order_by(
            desc(Post.created_at))

    return await paginate(
        session,
        request,
        params=params,
    )


@router.post('/user/{user_id}/posts', name='создание поста')
async def get_user_posts(
        post_data: PostCreateScheme,
        user_id: int = Path(...),
        current_user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{current_user.username} is\'t superuser or post author')
    post = Post(**post_data.dict(), user_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return PostShortScheme.from_orm(post)


@router.patch('/users/{user_id}/posts/{post_id}', response_model=PostUpdateScheme)
async def patch_post(user_id: int, post_id: int,
                     post_data: PostPatchScheme,
                     current_user: User = Depends(current_active_user),
                     session: AsyncSession = Depends(get_async_session)
                     ):
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{current_user.username} is\'t superuser or post author')

    new_data = post_data.dict(exclude_none=True)
    if not new_data:
        raise HTTPException(status_code=400, detail=f'empty data')
    query = select(Post).where(Post.id == post_id, Post.user_id == user_id)

    post = (await session.execute(query)).scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail='post not found')

    for key in new_data:
        setattr(post, key, new_data[key])

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return PostUpdateScheme.from_orm(post)


@router.delete('/users/{user_id}/posts/{post_id}', response_model=PostUpdateScheme)
async def delete_post(user_id: int, post_id: int,
                      current_user: User = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{current_user.username} is\'t superuser or post author')

    query = select(Post).where(Post.id == post_id, Post.user_id == user_id)

    post = (await session.execute(query)).scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail='post not found')

    await session.delete(post)
    await session.commit()
    return Response(status_code=204)
