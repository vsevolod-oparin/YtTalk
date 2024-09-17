import json
from abc import ABC
from pathlib import Path
from typing import Dict

from yt_talk.utils import load_json, save_json

DEEP_SEEK_KEY = 'deepseek'
TG_BOT_KEY = "telegram_bot"
LANGCHAIN_KEY = "langchain_key"


class SecretManager(ABC):

    def __init__(self, secret_pth: str = "secret.txt"):
        self.secret_pth = Path(secret_pth)
        self.store = self._fetch_store()

    def get_secret(self, name: str) -> str:
        return self.store.get(name, None)

    def store_secret(self, name: str, value: str) -> None:
        self.store[name] = value
        self._save_store()

    def _fetch_store(self) -> Dict[str, str]:
        if self.secret_pth.exists():
            return load_json(self.secret_pth)
        return dict()

    def _save_store(self) -> None:
        save_json(self.store, self.secret_pth, indent=2)


def main_init():
    sm = SecretManager()
    print(sm.get_secret(DEEP_SEEK_KEY))


if __name__ == '__main__':
    main_init()




