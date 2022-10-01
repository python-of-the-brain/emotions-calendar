from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.future import select

from db import User
from db.engine import get_async_session
from routers.schemes import UserRegisterScheme

router = APIRouter(
    tags=['Регистрация пользователя']
)

@router.post('/register', response_model=UserRegisterScheme, )
async def register_user(user: UserRegisterScheme,session = Depends(get_async_session)):
    q = select(User).where(User.email == user.email)

    u = (await session.execute(q)).scalars().first()
    if u is not None:
        raise HTTPException(status_code=400, detail='This email already is registered!')

    return user