import datetime
import uuid
from string import ascii_letters, digits

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field, validator, ValidationError
from typing import List, Optional

from db.mixins import TimestampMixin


class TimestampScheme(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserRegistrationScheme(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=25)
    remember: bool

    @validator('username')
    def username_validation(cls, data):
        for symbol in data:
            if symbol not in ascii_letters + digits + '_':
                raise ValidationError(f'username can\'t include {symbol}'
                                      f'(only ascii_letters, digits and \'_\' symbol)')
        return data


class UserLoginScheme(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=25)
    remember: bool


class UserRead(schemas.BaseUser[uuid.UUID]):
    email: EmailStr
    is_closed: bool = Field(default=False)
    username: str = Field(min_length=3, max_length=64)


class UserReadForComment(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    is_closed: bool = Field(default=False)
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=25)

    @validator('username')
    def username_validation(cls, data):
        for symbol in data:
            if symbol not in ascii_letters + digits + '_':
                raise ValidationError(f'username can\'t include {symbol}'
                                      f'(only ascii_letters, digits and \'_\' symbol)')
        return data


class UserUpdate(schemas.BaseUserUpdate):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)

    class Config:
        orm_mode = True


class PostCreateScheme(BaseModel):
    title: str = Field(max_length=64)
    content: str = Field(max_length=512)
    is_closed: Optional[bool] = Field(default=False)

    @validator('title')
    def space_validation_title(cls, data: str):
        return ' '.join(data.split())

    @validator('content')
    def space_validation_content(cls, data: str):
        return ' '.join(data.split())


class CommentShortScheme(TimestampScheme):
    id: int
    user_id: int
    post_id: int
    content: str

    class Config:
        orm_mode = True


class PostShortScheme(TimestampScheme):
    id: int
    title: str
    content: str
    is_closed: bool

    class Config:
        orm_mode = True


class PostPatchScheme(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_closed: Optional[bool]

    class Config:
        orm_mode = True


class EmotionStateReadScheme(BaseModel):
    name: str
    confidence: float

    class Config:
        orm_mode = True


class CommentReadScheme(BaseModel):
    id: int
    user: UserReadForComment
    content: str
    emotion: Optional[EmotionStateReadScheme]
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class CommentPostScheme(BaseModel):
    content: str
    emotion_id: Optional[int]

    class Config:
        orm_mode = True


class ShortObj(BaseModel):
    type_: str
    url: str

    class Config:
        orm_mode = True


class GetSearchObjs(BaseModel):
    count: int
    items: List[ShortObj]

    class Config:
        orm_mode = True


class PostReadScheme(TimestampScheme):
    id: int
    title: str
    content: str
    is_closed: bool
    comments: List[CommentReadScheme]
    emotion: Optional[EmotionStateReadScheme]

    class Config:
        orm_mode = True


class PostUpdateScheme(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    is_closed: Optional[bool]

    class Config:
        orm_mode = True


class PostStatisticResponse(BaseModel):
    items: List[PostCreateScheme]


class CurrentStatusScheme(BaseModel):
    value: Optional[str]
    emotion_id: Optional[int]

    class Config:
        orm_mode = True


class StatusScheme(BaseModel):
    value: str
    emotion_id: int = Field(gt=0)

    class Config:
        orm_mode = True


class CalendarDayScheme(BaseModel):
    day: datetime.date
    user_id: int
    emotion_id: Optional[int]

    class Config:
        orm_mode = True


class FavoriteScheme(BaseModel):
    user_id: int
    favourite_user_id: int

    class Config:
        orm_mode = True


class FavoritesScheme(BaseModel):
    item: List[FavoriteScheme]

    class Config:
        orm_mode = True


class ProfileScheme(BaseModel):
    user: UserReadForComment
    posts: List[PostReadScheme]
    current_status: CurrentStatusScheme
    previous_statuses: List[StatusScheme]
    calendar_days: List[CalendarDayScheme]

    class Config:
        orm_mode = True
