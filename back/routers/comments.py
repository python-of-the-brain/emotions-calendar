from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from controllers.users import current_active_user
from db.engine import get_async_session
from db.models import Post, User, Comment
from routers.shemas import CommentPostScheme, CommentShortScheme

router = APIRouter(tags=['Комментарии'])


@router.post('/users/{user_id}/posts/{post_id}/comments')
async def get_comments(
        user_id: int,
        post_id: int,
        comment_data: CommentPostScheme,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    author = await session.get(User, user_id)

    if author is None:
        raise HTTPException(status_code=404, detail='user not found')

    if user.id != user_id and not user.is_superuser and author.is_closed:
        raise HTTPException(status_code=403, detail='Access denied')

    post = await session.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='post not found')

    if post.is_closed and not user.is_superuser and post.user_id != user.id:
        raise HTTPException(status_code=403, detail='Access denied')

    comment = Comment(**comment_data.dict(), user_id=user.id, post_id=post_id)

    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return CommentShortScheme.from_orm(comment)


@router.delete('/users/{user_id}/posts/{post_id}/comment/{comment_id}')
async def delete_comment(
        user_id: int,
        post_id: int,
        comment_id: int,
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    author = await session.get(User, user_id)

    if author is None:
        raise HTTPException(status_code=404, detail='user not found')

    if user.id != user_id and not user.is_superuser:
        raise HTTPException(status_code=403, detail='Access denied')

    post = await session.get(Post, post_id)

    if post is None:
        raise HTTPException(status_code=404, detail='post not found')

    if post.is_closed and post.user_id != user_id and not user.is_superuser:
        raise HTTPException(status_code=403, detail='Access denied')

    comment = await session.get(Comment, comment_id)

    if comment is None:
        raise HTTPException(status_code=404, detail='comment not found')

    if comment.user_id != user_id and not user.is_superuser:
        raise HTTPException(status_code=403, detail='Access denied')

    await session.delete(comment)
    await session.commit()
    return Response(status_code=204)
