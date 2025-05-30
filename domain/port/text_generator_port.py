from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class TextGeneratorPort(ABC):
    
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: List[Dict[str, str]]) -> str:
        pass
    
    @abstractmethod
    def generate_text_with_context(self, prompt: str, chat_history: List[Dict[str, str]], 
                                   context: str, user_id: Optional[str] = None) -> str:
        pass