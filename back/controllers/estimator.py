import statistics

from controllers.monkey_learn_api import MonkeyLearnAPI, EmotionalState
from controllers.translator_api import TranslatorAPI


class Estimator:
    def __init__(self) -> None:
        self.monkey_learn_api = MonkeyLearnAPI()
        self.translator_api = TranslatorAPI()


    def get_estimate(self, text: str) -> EmotionalState:
        translated_text = self.translator_api.get_translate(text=text)
        d: dict = {state.value: 0 for state in EmotionalState }
        for sentence in translated_text.split('.'):
            e = self.monkey_learn_api.get_estimate(text=sentence)
            if e is not None:
                d[e.name] += e.confidence
        return EmotionalState(max(d, key=d.get))

        