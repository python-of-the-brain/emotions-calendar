
from config import get_settings


class MonkeyLearnAPI:

    def __init__(self) -> None:
        settings = get_settings()

        self.token = settings.MONKEY_LEARN_API

    

