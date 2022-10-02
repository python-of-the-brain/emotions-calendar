import re
from typing import Dict, Optional

import requests

from config import get_settings


class TranslatorAPI:
    def __init__(self):
        settings = get_settings()
        self.TRANSLATER_URL = settings.TRANSLATER_URL

    def _get_translate(self, text: str, from_: str = 'ru', to: str = 'en') -> Optional[Dict]:
        result = requests.post(
            url=self.TRANSLATER_URL,
            json={
                "from": from_,
                "to": to,
                "text": text,
            },
            headers={'Content-Type': 'application/json'},
        )
        if result.ok:
            return result.json()
        print(result.text)
        return None

    def get_translate(self, text: str) -> str:
        sentences = text.split('.')
        results = []
        for sentence in sentences:
            result = self._get_translate(text=sentence)
            if result is not None:
                results.append(re.sub(r'\.+$', '', result.get('result')))
        print(results)
        return '. '.join(results)
