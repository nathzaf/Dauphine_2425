import unittest
from unittest.mock import MagicMock

from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.model.rag_query import RAGQuery, RAGResult
from domain.model.document_chunk import DocumentChunk
from domain.port.chat_application_port import ChatApplicationPort
from domain.service.rag_service import RAGService
from domain.service.rag_chat_service import RAGChatService


class TestRAGChatService(unittest.TestCase):
    def setUp(self):
        # Create mocks for dependencies
        self.rag_service_mock = MagicMock(spec=RAGService)
        self.chat_application_mock = MagicMock(spec=ChatApplicationPort)
        
        # Create the service with mocked dependencies
        self.rag_chat_service = RAGChatService(
            rag_service=self.rag_service_mock,
            chat_application=self.chat_application_mock
        )

    def test_chat_with_rag_success(self):
        # Given: a chat message and existing history
        message = "What is machine learning?"
        chat_id = "chat-123"
        
        # Mock existing chat history
        existing_history = History(chat_id, [
            RoleMessage("user", "Hello"),
            RoleMessage("assistant", "Hi there!")
        ])
        
        # Mock RAG result
        rag_result = RAGResult(
            query=RAGQuery(message, chat_id),
            relevant_chunks=[
                DocumentChunk("chunk-1", "doc-1", "ML is a subset of AI", 0)
            ],
            generated_response="Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
            confidence_score=0.8
        )
        
        self.chat_application_mock.get_history.return_value = existing_history
        self.rag_service_mock.query_with_rag.return_value = rag_result

        # When: chatting with RAG
        result = self.rag_chat_service.chat_with_rag(message, chat_id)

        # Then: returns generated response and updates history
        self.assertEqual(result, rag_result.generated_response)
        
        # Verify RAG service was called with correct parameters
        self.rag_service_mock.query_with_rag.assert_called_once_with(
            query=message,
            chat_id=chat_id,
            chat_history=existing_history,
            max_chunks=5,
            similarity_threshold=0.7
        )
        
        # Verify history was updated with user and assistant messages
        self.assertEqual(len(existing_history.chat_history), 4)  # 2 existing + 2 new
        
        # Check the new messages
        user_message = existing_history.chat_history[2]
        assistant_message = existing_history.chat_history[3]
        
        self.assertEqual(user_message.role, "user")
        self.assertEqual(user_message.message, message)
        self.assertEqual(assistant_message.role, "assistant")
        self.assertEqual(assistant_message.message, rag_result.generated_response)
        
        # Verify history was saved
        self.chat_application_mock.save_history.assert_called_once_with(existing_history)

    def test_chat_with_rag_custom_parameters(self):
        # Given: custom parameters for RAG
        message = "Explain neural networks"
        chat_id = "chat-456"
        max_chunks = 3
        similarity_threshold = 0.8
        
        existing_history = History(chat_id, [])
        rag_result = RAGResult(
            query=RAGQuery(message, chat_id),
            relevant_chunks=[],
            generated_response="Neural networks are computational models inspired by biological neural networks.",
            confidence_score=0.6
        )
        
        self.chat_application_mock.get_history.return_value = existing_history
        self.rag_service_mock.query_with_rag.return_value = rag_result

        # When: chatting with custom parameters
        result = self.rag_chat_service.chat_with_rag(
            message, chat_id, max_chunks=max_chunks, similarity_threshold=similarity_threshold
        )

        # Then: uses custom parameters
        self.assertEqual(result, rag_result.generated_response)
        
        self.rag_service_mock.query_with_rag.assert_called_once_with(
            query=message,
            chat_id=chat_id,
            chat_history=existing_history,
            max_chunks=max_chunks,
            similarity_threshold=similarity_threshold
        )

    def test_chat_with_rag_empty_history(self):
        # Given: empty chat history
        message = "First message"
        chat_id = "new-chat"
        
        empty_history = History(chat_id, [])
        rag_result = RAGResult(
            query=RAGQuery(message, chat_id),
            relevant_chunks=[],
            generated_response="Hello! How can I help you?",
            confidence_score=0.0
        )
        
        self.chat_application_mock.get_history.return_value = empty_history
        self.rag_service_mock.query_with_rag.return_value = rag_result

        # When: chatting with empty history
        result = self.rag_chat_service.chat_with_rag(message, chat_id)

        # Then: history is properly initialized and updated
        self.assertEqual(result, rag_result.generated_response)
        self.assertEqual(len(empty_history.chat_history), 2)  # user + assistant messages

    def test_get_chat_context_info(self):
        # Given: a chat with available documents
        chat_id = "chat-789"
        available_documents = ["document1.pdf (pdf)", "image1.jpg (image)", "document2.pdf (pdf)"]
        
        self.rag_service_mock.get_document_context_for_chat.return_value = available_documents

        # When: getting chat context info
        result = self.rag_chat_service.get_chat_context_info(chat_id)

        # Then: returns formatted context information
        expected_result = {
            "chat_id": chat_id,
            "available_documents": available_documents,
            "document_count": 3
        }
        
        self.assertEqual(result, expected_result)
        self.rag_service_mock.get_document_context_for_chat.assert_called_once_with(chat_id)

    def test_get_chat_context_info_no_documents(self):
        # Given: a chat with no documents
        chat_id = "empty-chat"
        
        self.rag_service_mock.get_document_context_for_chat.return_value = []

        # When: getting chat context info
        result = self.rag_chat_service.get_chat_context_info(chat_id)

        # Then: returns empty context information
        expected_result = {
            "chat_id": chat_id,
            "available_documents": [],
            "document_count": 0
        }
        
        self.assertEqual(result, expected_result)

    def test_chat_with_rag_preserves_message_order(self):
        # Given: existing conversation
        message = "Continue our discussion"
        chat_id = "chat-conversation"
        
        existing_history = History(chat_id, [
            RoleMessage("user", "What is AI?"),
            RoleMessage("assistant", "AI is artificial intelligence."),
            RoleMessage("user", "Tell me more about machine learning.")
        ])
        
        rag_result = RAGResult(
            query=RAGQuery(message, chat_id),
            relevant_chunks=[],
            generated_response="Machine learning is a subset of AI that focuses on algorithms that can learn from data.",
            confidence_score=0.7
        )
        
        self.chat_application_mock.get_history.return_value = existing_history
        self.rag_service_mock.query_with_rag.return_value = rag_result

        # When: continuing the conversation
        result = self.rag_chat_service.chat_with_rag(message, chat_id)

        # Then: messages are added in correct order
        self.assertEqual(len(existing_history.chat_history), 5)  # 3 existing + 2 new
        
        # Verify the order is preserved
        self.assertEqual(existing_history.chat_history[3].role, "user")
        self.assertEqual(existing_history.chat_history[3].message, message)
        self.assertEqual(existing_history.chat_history[4].role, "assistant")
        self.assertEqual(existing_history.chat_history[4].message, rag_result.generated_response)


if __name__ == '__main__':
    unittest.main() 