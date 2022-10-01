from fastapi_users.db import SQLAlchemyBaseUserTable

from db.base import Base

__all__ = ['User']


class User(SQLAlchemyBaseUserTable, Base):
    pass