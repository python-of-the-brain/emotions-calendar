from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from controllers.estimator import Estimator
from controllers.monkey_learn_api import MonkeyLearnAPI, MonkeyLearnResult

from controllers.translator_api import TranslatorAPI

__all__ = ['external_api_router']

external_api_router = APIRouter(prefix='/external', tags=['External API'])


class TranslateResponse(BaseModel):
    result: str


@external_api_router.post(path='/translate', response_model=TranslateResponse)
async def post_translate(
        from_=Query(alias='from', default='ru', title='Исходный язык'),
        to=Query(default='en', title='На какой перевести'),
        text=Query(default='Мама мыла раму', title='Текст')
):
    return TranslatorAPI()._get_translate(text=text, from_=from_, to=to)


@external_api_router.post(path='/classify', response_model=MonkeyLearnResult)
async def post_classify(
        text: str = Query(
            default='Happy New Year!',
            min_length=5,
            max_length=1000,
        )
):
    return MonkeyLearnAPI().get_estimate(text=text)


@external_api_router.post(path='/estimator', response_model=Optional[TranslateResponse])
async def post_estimator(text: str = Query(default='', title='Текст для оценки эмоции')):
    """
    Запрос прогоняет текст через переводчик и модель оценивающую эмоциональный окрас текста, на основе которого
    мы делаем вывод об эмоциях пользователя.
    """
    estimator = Estimator()
    result = estimator.get_estimate(text=text)
    return TranslateResponse(result=result)

