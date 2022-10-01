from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.engine import get_async_session
from db.models import User

router = APIRouter()


@router.get('/get_user/{id}/',
            name='Получает информацию о пользователе по id')
def get_unit(id: int, session: Session = Depends(get_async_session)):
    user = session.query(User).get(id)