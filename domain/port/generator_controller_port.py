from abc import ABC, abstractmethod

from domain.model.history import History
from rest.model.role_message_request import RoleMessageRequest


class GeneratorControllerPort(ABC):
    @abstractmethod
    def generate_message(self, prompt: str, chat_history: list[RoleMessageRequest]) -> str:
        pass

    @abstractmethod
    def save_history(self, history: History):
        pass

    @abstractmethod
    def get_history(self, chat_id: str) -> History:
        pass

    @abstractmethod
    def get_all_histories(self) -> list[History]:
        pass
