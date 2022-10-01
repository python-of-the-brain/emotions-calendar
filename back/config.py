from functools import lru_cache
from pydantic import BaseSettings, Field



class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='Python головного мозга')
    DEBUG: bool = Field(default=True)
    VERSION: str = Field(default='0.0.1')




@lru_cache
def get_settings() -> Settings:

    return Settings()