from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='Python головного мозга')
    DEBUG: bool = Field(default=True)
    VERSION: str = Field(default='0.0.1')

    SECRET: str = Field(default='secret')

    POSTGRES_DB: str = Field(default='dev')
    POSTGRES_USER: str = Field(default='user')
    POSTGRES_PASSWORD: str = Field(default='secret')
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: str = Field(default='5432')

    SQLALCHEMY_URL: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_URL', pre=True)
    def get_sqlalchemy_url(cls, v, values): 
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    MONKEY_LEARN_API: str 

    TRANSLATOR_SCHEME: str = Field(default='http')
    TRANSLATOR_HOST: str = Field(default='127.0.0.1')
    TRANSLATOR_PORT: str = Field(default=8082)

    @property
    def TRANSLATOR_URL(self) -> str:
        return f'{self.TRANSLATOR_SCHEME}://{self.TRANSLATOR_HOST}:{self.TRANSLATOR_PORT}/v1/translate'

@lru_cache
def get_settings() -> Settings:
    return Settings()