import enum
from loguru import logger
from pydantic import BaseModel, Extra, Field
import requests
from typing import Optional

from config import get_settings


class EmotionalState(str, enum.Enum):
    negative = 'Negative'
    neutral = 'Neutral'
    positive = 'Positive'


class MonkeyLearnResult(BaseModel):
    confidence: float
    name: EmotionalState = Field(alias='tag_name')

    class Config:
        use_enum_values = True
        extra = Extra.ignore


class MonkeyLearnAPI:
    HOST = 'https://api.monkeylearn.com'
    VERSION = 'v3'
    PATH = 'classifiers'
    MODEL = 'cl_pi3C7JiL'
    METHOD = 'classify'

    def __init__(self) -> None:
        settings = get_settings()
        self.token = settings.MONKEY_LEARN_API

    @property
    def API_URL(self) -> str:
        return f'{self.HOST}/{self.VERSION}/{self.PATH}/{self.MODEL}/{self.METHOD}/'

    def get_estimate(self, text: str) -> Optional[MonkeyLearnResult]:
        result = requests.post(
            url=self.API_URL,
            headers={'Authorization': f'Token {self.token}'},
            json={"data": [text]},
        )
        if result.ok:
            return MonkeyLearnResult.parse_obj(result.json()[0].get('classifications')[0])
        logger.warning(result.json())
        return None
