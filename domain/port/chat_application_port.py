from abc import abstractmethod, ABC

from domain.model.history import History


class ChatApplicationPort(ABC):

    @abstractmethod
    def get_generated_text(self, prompt: str, chat_history: History) -> str:
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
