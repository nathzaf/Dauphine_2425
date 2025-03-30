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
    def create_conversation(self) -> str:
        pass
    
    @abstractmethod
    def get_history(self, conversation_guid: str) -> ChatHistory:
        pass
    
    @abstractmethod
    def generate_message_in_conversation(self, conversation_guid: str, prompt: str) -> ChatHistory:
        pass
    
    @abstractmethod
    def clear_history(self, conversation_guid: str) -> ChatHistory:
        pass