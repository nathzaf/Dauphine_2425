from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.service.rag_service import RAGService
from domain.port.chat_application_port import ChatApplicationPort


class RAGChatService:
    def __init__(
        self,
        rag_service: RAGService,
        chat_application: ChatApplicationPort
    ):
        self.rag_service = rag_service
        self.chat_application = chat_application

    def chat_with_rag(
        self,
        message: str,
        chat_id: str,
        max_chunks: int = 5,
        similarity_threshold: float = 0.7
    ) -> str:
        """Handle a chat message with RAG capabilities"""
        # Get chat history
        chat_history = self.chat_application.get_history(chat_id)

        # Perform RAG query
        rag_result = self.rag_service.query_with_rag(
            query=message,
            chat_id=chat_id,
            chat_history=chat_history, 
            max_chunks=max_chunks,
            similarity_threshold=similarity_threshold
        )

        # Add user message to history
        user_message = RoleMessage(role="user", message=message)
        chat_history.add(user_message)

        # Add assistant response to history
        assistant_message = RoleMessage(role="assistant", message=rag_result.generated_response)
        chat_history.add(assistant_message)

        # Save updated history
        self.chat_application.save_history(chat_history)

        return rag_result.generated_response

    def get_chat_context_info(self, chat_id: str) -> dict:
        """Get information about available documents and context for a chat"""
        documents = self.rag_service.get_document_context_for_chat(chat_id)
        return {
            "chat_id": chat_id,
            "available_documents": documents,
            "document_count": len(documents)
        } 