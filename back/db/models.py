import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from db.base import Base
from db.engine import get_async_session
from db.mixins import IsClosedMixin, TimestampMixin, SearchMixin

__all__ = ['User', 'Emotion', 'Base', 'Post', 'CalendarDay', 'Comment', 'Status', 'get_user_db', 'FavouriteUser']


class Emotion(Base):
    name = Column(String(64), index=True, nullable=False)
    src = Column(String(512), nullable=False)


class User(TimestampMixin, IsClosedMixin, SearchMixin, SQLAlchemyBaseUserTable, Base):
    username = Column(String(64), index=True, nullable=False)

    posts = relationship('Post', back_populates='user', order_by='Post.created_at.desc()')
    comments = relationship('Comment', back_populates='user')
    statuses = relationship('Status', back_populates='user')
    calendar_days = relationship('CalendarDay', back_populates='user')

    @property
    def url(self) -> str:
        return f'/users/{self.id}/profile'

    favourite_users = relationship('User', secondary='favourite_user', foreign_keys='FavouriteUser.favourite_user_id')


class FavouriteUser(Base):
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    favourite_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)


class Post(TimestampMixin, SearchMixin, IsClosedMixin, Base):
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    emotion_id = Column(ForeignKey('emotion.id'), index=True, nullable=True)
    title = Column(String(256), index=True, nullable=False)
    content = Column(String(2048), index=True, nullable=False)

    comments = relationship('Comment', back_populates='post', order_by='Comment.created_at.desc()')
    user = relationship('User', back_populates='posts')
    emotion = relationship('Emotion')

    @property
    def url(self) -> str:
        return f'/users/{self.user_id}/posts/{self.id}/'


class CalendarDay(Base):
    day = Column(Date, index=True, default=datetime.date.today, nullable=False)

    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    emotion_id = Column(ForeignKey('emotion.id'), index=True, nullable=True)

    user = relationship('User', back_populates='calendar_days')
    emotion = relationship('Emotion')


class Comment(TimestampMixin, Base):
    content = Column(String)

    post_id = Column(ForeignKey('post.id'), index=True, nullable=False)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    emotion_id = Column(ForeignKey('emotion.id'), index=True, nullable=True)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    emotion = relationship('Emotion')


class Status(TimestampMixin, IsClosedMixin, Base):
    value = Column(String(255), index=True, nullable=True)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    emotion_id = Column(ForeignKey('emotion.id'), index=True, nullable=True)

    user = relationship('User', back_populates='statuses')


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
