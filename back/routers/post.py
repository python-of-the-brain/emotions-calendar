import loguru
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.users import current_active_user
from routers.shemas import PostStatisticResponse, PostCreateScheme, PostUpdateScheme
from db.engine import get_async_session
from db.models import Post, User

router = APIRouter()


@router.get('/user/{user_id}/posts',
            name='возвращает posts пользователя')
async def get_user_posts(user_id: int, user: User = Depends(current_active_user),
                         session: AsyncSession = Depends(get_async_session)
):
    statement = select(Post).where(Post.user_id == user_id)
    posts = (await session.execute(statement)).all()
    return PostStatisticResponse(items=posts)


@router.post('/user/{user_id}/posts', name='создание поста')
async def get_user_posts(
        post_data: PostCreateScheme,
        user_id: int = Path(...),
        cuurent_user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):
    if cuurent_user.id != user_id and not cuurent_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{cuurent_user.username} is\'t superuser or post author')
    post = Post(**post_data.dict(), user_id=user_id)
    session.add(post)
    return {'status': 'ok'}


@router.patch('users/{user_id}/posts/{post_id}')
def patch_post(user_id: int, post_id: int,
               post_data: PostUpdateScheme,
               cuurent_user: User = Depends(current_active_user),
               session: AsyncSession = Depends(get_async_session)
):
    if cuurent_user.id != user_id and not cuurent_user.is_superuser:
        raise HTTPException(status_code=403, detail=f'{cuurent_user.username} is\'t superuser or post author')
    loguru.logger.warning(post_data.dict())
    for field in post_data.dict():
        pass
