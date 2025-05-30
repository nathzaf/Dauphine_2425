from domain.model.history import History
from domain.port.chat_application_port import ChatApplicationPort
from typing import Optional, Dict, Any


class TextGenerationService:
    def __init__(self, chat_application_port: ChatApplicationPort = None):
        self.chat_application_port = chat_application_port

    def get_generated_text(self, prompt: str, chat_history: History) -> str:
        return self.chat_application_port.get_generated_text(prompt, chat_history)
    
    def get_generated_text_with_context(self, prompt: str, chat_history: History, 
                                       user_id: Optional[str] = None, 
                                       user_context: Optional[Dict[str, Any]] = None) -> str:
        # Check if the chat application adapter supports context
        if hasattr(self.chat_application_port, 'get_generated_text_with_context'):
            return self.chat_application_port.get_generated_text_with_context(
                prompt, chat_history, user_id=user_id, user_context=user_context
            )
        else:
            return self.chat_application_port.get_generated_text(prompt, chat_history)
