from abc import ABC, abstractmethod

from domain.model.chat_history import ChatHistory

class TextGeneratorPort(ABC):
    @abstractmethod
    def get_generated_text(self, chat_history: ChatHistory) -> str:
        pass