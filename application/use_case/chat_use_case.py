from typing import List, Optional, Dict, Any
from domain.service.rag_service import RAGService
from domain.service.history_service import HistoryService
from domain.model.history import History
from domain.model.role_message import RoleMessage

class ChatUseCase:
    def __init__(self, rag_service: RAGService, history_service: HistoryService):
        self.rag_service = rag_service
        self.history_service = history_service

    def generate_chat_response(self, prompt: str, chat_history: List[Dict[str, str]], 
                             user_id: Optional[str] = None, 
                             user_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a chat response using RAG"""
        return self.rag_service.generate_contextual_response(
            prompt=prompt,
            chat_history=chat_history,
            user_id=user_id,
            user_context=user_context
        )

    def save_conversation(self, chat_id: str, messages: List[Dict[str, str]]):
        """Save conversation history"""
        role_messages = [
            RoleMessage(role=msg["role"], message=msg["message"]) 
            for msg in messages
        ]
        history = History(chat_id=chat_id, chat_history=role_messages)
        self.history_service.save_history(history)

    def get_conversation_history(self, chat_id: str) -> History:
        """Retrieve conversation history"""
        return self.history_service.get_history(chat_id)

    def get_all_conversations(self) -> List[History]:
        """Get all conversation histories"""
        return self.history_service.get_all_histories() 