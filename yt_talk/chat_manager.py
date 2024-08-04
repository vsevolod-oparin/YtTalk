import json
import plyvel

from openai import OpenAI
from typing import List, Tuple, Optional

from .ai import get_ai_response


class ChatManager:

    def __init__(
            self,
            client: OpenAI,
            db: plyvel.DB):
        self.client = client
        self.db = db

    def init_chat(
            self,
            name: str,
            transcription: str,
            highlight_num: int) -> Tuple[str, List]:
        response, history = get_ai_response(
            client=self.client,
            transcription=transcription,
            highlight_num=highlight_num,
            history_list=None
        )
        self._set_history(name, history)
        return response, history

    def add_message(self, name: str, message: str) -> Tuple[str, List]:
        history = self._get_history(name)
        response, history = get_ai_response(
            client=self.client,
            message=message,
            history_list=history,
        )
        self._set_history(name, history)
        return response, history

    def get_chat(self, name: str) -> List:
        chat = self._get_history(name)[2:]
        return [msg['content'] for msg in chat]

    def get_coupled_chat(self, name) -> List:
        chat = self.get_chat(name)
        if len(chat) % 2 == 1:
            chat = [None] + chat
        return [
            chat[i: i + 2]
            for i in range(0, len(chat), 2)
        ]

    def forget_chat(self, name: str) -> None:
        chat_start = self._get_history(name)[:3]
        self._set_history(name, chat_start)

    def _get_history(self, name: str) -> Optional[List]:
        history_str = self._get(f"HISTORY_{name}")
        if history_str is None:
            return None
        return json.loads(history_str)

    def _set_history(self, name: str, history: List) -> None:
        history_str = json.dumps(history)
        self._put(f"HISTORY_{name}", history_str)

    def _put(self, key_str: str, value_str: str):
        self.db.put(
            key_str.encode('utf-8'),
            value_str.encode('utf-8'),
        )

    def _get(self, key_str: str) -> Optional[str]:
        value = self.db.get(
            key_str.encode('utf-8')
        )
        if value is None:
            return None
        return value.decode('utf-8')

