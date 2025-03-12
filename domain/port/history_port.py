from abc import ABC, abstractmethod
from typing import List, Dict

class HistoryPort(ABC):
    @abstractmethod
    def save_message(self, conversation_id: str, role: str, message: str):
        pass

    @abstractmethod
    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def clear_history(self, conversation_id: str):
        pass