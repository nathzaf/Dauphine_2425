from abc import ABC, abstractmethod

from domain.model.chat_history import ChatHistory

class GeneratorControllerPort(ABC):
    @abstractmethod
    def generate_message(self, prompt: str) -> str:
        pass
    
    @abstractmethod
    def get_conversations(self) -> list[str]:
        pass
    
    @abstractmethod
    def get_history(self, conversation_guid: str) -> ChatHistory:
        pass
    
    @abstractmethod
    def clear_history(self, conversation_guid: str) -> ChatHistory:
        pass