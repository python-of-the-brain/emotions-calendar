import uuid
from string import ascii_letters, digits

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field, validator, ValidationError
from typing import List, Optional


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
    username: str = Field(min_length=3, max_length=64)
    pass


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
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


class PostUpdateScheme(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_closed: Optional[bool]


class PostStatisticResponse(BaseModel):
    items: List[PostCreateScheme]
