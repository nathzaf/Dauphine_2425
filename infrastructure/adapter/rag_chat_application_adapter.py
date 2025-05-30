from domain.model.history import History
from domain.port.chat_application_port import ChatApplicationPort
from infrastructure.history_repository.history_repository import HistoryRepository
from infrastructure.text_generator.rag_cohere_text_generator import RAGCohereTextGenerator
from typing import Optional, Dict, Any

class RAGChatApplicationAdapter(ChatApplicationPort):

    def __init__(self,
                 text_generator: RAGCohereTextGenerator = None,
                 history_repository: HistoryRepository = None):
        self.text_generator = text_generator
        self.history_repository = history_repository

    def get_generated_text(self, prompt: str, chat_history: History) -> str:
        return self.text_generator.generate_text_with_context(
            prompt=prompt, 
            chat_history=chat_history.chat_history
        )
    
    def get_generated_text_with_context(self, prompt: str, chat_history: History, 
                                       user_id: Optional[str] = None, 
                                       user_context: Optional[Dict[str, Any]] = None) -> str:
        return self.text_generator.generate_text_with_context(
            prompt=prompt, 
            chat_history=chat_history.chat_history,
            user_id=user_id,
            user_context=user_context
        )

    def save_history(self, history: History):
        self.history_repository.save_history(history)

    def get_history(self, chat_id: str) -> History:
        return self.history_repository.get_history(chat_id)

    def get_all_histories(self) -> list[History]:
        return self.history_repository.get_all_histories() 