import datetime

from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    """Mixin with timestamp fields"""
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        server_onupdate=func.now(), 
        onupdate=datetime.datetime.now
    )


@declarative_mixin
class IsClosedMixin:
    is_closed = Column(Boolean, default=False, index=True)


@declarative_mixin
class SearchMixin:

    @property
    def type_(self) -> str:
        return self.__class__.__name__

    @property
    def url(self) -> str:
        raise NotImplemented
