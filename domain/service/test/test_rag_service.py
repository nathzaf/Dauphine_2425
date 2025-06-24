import unittest
from unittest.mock import MagicMock
from typing import List

from domain.model.document import Document, DocumentStatus, DocumentType
from domain.model.document_chunk import DocumentChunk
from domain.model.rag_query import RAGQuery, RAGResult
from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.embedding_service_port import EmbeddingServicePort
from domain.port.rag_generator_port import RAGGeneratorPort
from domain.service.document_service import DocumentService
from domain.service.rag_service import RAGService


class TestRAGService(unittest.TestCase):
    def setUp(self):
        # Create mocks for all dependencies
        self.chunk_repository_mock = MagicMock(spec=DocumentChunkRepositoryPort)
        self.embedding_service_mock = MagicMock(spec=EmbeddingServicePort)
        self.rag_generator_mock = MagicMock(spec=RAGGeneratorPort)
        self.document_service_mock = MagicMock(spec=DocumentService)
        
        # Create the service with mocked dependencies
        self.rag_service = RAGService(
            chunk_repository=self.chunk_repository_mock,
            embedding_service=self.embedding_service_mock,
            rag_generator=self.rag_generator_mock,
            document_service=self.document_service_mock
        )

    def test_query_with_rag_no_documents_uses_fallback(self):
        # Given: no processed documents for the chat
        query = "What is machine learning?"
        chat_id = "chat-123"
        chat_history = History(chat_id, [])
        fallback_response = "I don't have specific documents to reference, but machine learning is..."
        
        self.document_service_mock.get_processed_documents_for_chat.return_value = []
        self.rag_generator_mock.generate_response_without_context.return_value = fallback_response

        # When: querying with RAG
        result = self.rag_service.query_with_rag(query, chat_id, chat_history)

        # Then: uses fallback generation
        self.assertIsInstance(result, RAGResult)
        self.assertEqual(result.generated_response, fallback_response)
        self.assertEqual(len(result.relevant_chunks), 0)
        self.assertEqual(result.confidence_score, 0.0)
        
        self.document_service_mock.get_processed_documents_for_chat.assert_called_once_with(chat_id)
        self.rag_generator_mock.generate_response_without_context.assert_called_once_with(query, chat_history)

    def test_query_with_rag_with_relevant_chunks(self):
        # Given: processed documents and relevant chunks exist
        query = "What is machine learning?"
        chat_id = "chat-123"
        chat_history = History(chat_id, [])
        
        # Mock processed documents
        processed_docs = [
            Document("doc-1", "ml_guide.pdf", DocumentType.PDF, "/path1", chat_id, DocumentStatus.PROCESSED)
        ]
        
        # Mock query embedding
        query_embedding = [0.1, 0.2, 0.3]
        
        # Mock relevant chunks
        relevant_chunks = [
            DocumentChunk("chunk-1", "doc-1", "Machine learning is a subset of AI", 0, [0.15, 0.25, 0.35]),
            DocumentChunk("chunk-2", "doc-1", "It involves training algorithms on data", 1, [0.12, 0.22, 0.32])
        ]
        
        # Mock generated response
        generated_response = "Based on the documents, machine learning is a subset of AI that involves training algorithms on data."
        
        self.document_service_mock.get_processed_documents_for_chat.return_value = processed_docs
        self.embedding_service_mock.generate_embedding.return_value = query_embedding
        self.chunk_repository_mock.search_similar_chunks.return_value = relevant_chunks
        self.rag_generator_mock.generate_response_with_context.return_value = generated_response
        self.embedding_service_mock.calculate_similarity.side_effect = [0.8, 0.7]  # Mock similarities

        # When: querying with RAG
        result = self.rag_service.query_with_rag(query, chat_id, chat_history)

        # Then: uses context-based generation
        self.assertIsInstance(result, RAGResult)
        self.assertEqual(result.generated_response, generated_response)
        self.assertEqual(len(result.relevant_chunks), 2)
        self.assertEqual(result.confidence_score, 0.75)  # Average of 0.8 and 0.7
        
        # Verify method calls
        self.embedding_service_mock.generate_embedding.assert_called_once_with(query)
        self.chunk_repository_mock.search_similar_chunks.assert_called_once_with(
            query_embedding=query_embedding,
            chat_id=chat_id,
            max_results=5,
            similarity_threshold=0.7
        )
        self.rag_generator_mock.generate_response_with_context.assert_called_once_with(
            query, relevant_chunks, chat_history
        )

    def test_query_with_rag_no_relevant_chunks_uses_fallback(self):
        # Given: processed documents exist but no relevant chunks found
        query = "What is quantum computing?"
        chat_id = "chat-123"
        chat_history = History(chat_id, [])
        
        processed_docs = [
            Document("doc-1", "ml_guide.pdf", DocumentType.PDF, "/path1", chat_id, DocumentStatus.PROCESSED)
        ]
        
        query_embedding = [0.1, 0.2, 0.3]
        fallback_response = "I don't have relevant information about quantum computing in the uploaded documents."
        
        self.document_service_mock.get_processed_documents_for_chat.return_value = processed_docs
        self.embedding_service_mock.generate_embedding.return_value = query_embedding
        self.chunk_repository_mock.search_similar_chunks.return_value = []  # No relevant chunks
        self.rag_generator_mock.generate_response_without_context.return_value = fallback_response

        # When: querying with RAG
        result = self.rag_service.query_with_rag(query, chat_id, chat_history)

        # Then: uses fallback generation
        self.assertEqual(result.generated_response, fallback_response)
        self.assertEqual(len(result.relevant_chunks), 0)
        self.assertEqual(result.confidence_score, 0.0)
        
        self.rag_generator_mock.generate_response_without_context.assert_called_once_with(query, chat_history)

    def test_query_with_rag_custom_parameters(self):
        # Given: custom parameters for RAG query
        query = "What is AI?"
        chat_id = "chat-123"
        chat_history = History(chat_id, [])
        max_chunks = 3
        similarity_threshold = 0.8
        
        processed_docs = [Document("doc-1", "ai.pdf", DocumentType.PDF, "/path1", chat_id, DocumentStatus.PROCESSED)]
        query_embedding = [0.1, 0.2, 0.3]
        relevant_chunks = [DocumentChunk("chunk-1", "doc-1", "AI content", 0, [0.1, 0.2, 0.3])]
        
        self.document_service_mock.get_processed_documents_for_chat.return_value = processed_docs
        self.embedding_service_mock.generate_embedding.return_value = query_embedding
        self.chunk_repository_mock.search_similar_chunks.return_value = relevant_chunks
        self.rag_generator_mock.generate_response_with_context.return_value = "AI response"
        self.embedding_service_mock.calculate_similarity.return_value = 0.9

        # When: querying with custom parameters
        result = self.rag_service.query_with_rag(
            query, chat_id, chat_history, max_chunks=max_chunks, similarity_threshold=similarity_threshold
        )

        # Then: uses custom parameters
        self.chunk_repository_mock.search_similar_chunks.assert_called_once_with(
            query_embedding=query_embedding,
            chat_id=chat_id,
            max_results=max_chunks,
            similarity_threshold=similarity_threshold
        )

    def test_calculate_confidence_score_no_chunks(self):
        # Given: no chunks
        query_embedding = [0.1, 0.2, 0.3]
        chunks = []

        # When: calculating confidence score
        score = self.rag_service._calculate_confidence_score(query_embedding, chunks)

        # Then: returns 0.0
        self.assertEqual(score, 0.0)

    def test_calculate_confidence_score_with_chunks(self):
        # Given: chunks with embeddings
        query_embedding = [0.1, 0.2, 0.3]
        chunks = [
            DocumentChunk("chunk-1", "doc-1", "content1", 0, [0.15, 0.25, 0.35]),
            DocumentChunk("chunk-2", "doc-1", "content2", 1, [0.12, 0.22, 0.32])
        ]
        
        self.embedding_service_mock.calculate_similarity.side_effect = [0.8, 0.6]

        # When: calculating confidence score
        score = self.rag_service._calculate_confidence_score(query_embedding, chunks)

        # Then: returns average similarity
        self.assertEqual(score, 0.7)  # (0.8 + 0.6) / 2

    def test_calculate_confidence_score_chunks_without_embeddings(self):
        # Given: chunks without embeddings
        query_embedding = [0.1, 0.2, 0.3]
        chunks = [
            DocumentChunk("chunk-1", "doc-1", "content1", 0),  # No embedding
            DocumentChunk("chunk-2", "doc-1", "content2", 1)   # No embedding
        ]

        # When: calculating confidence score
        score = self.rag_service._calculate_confidence_score(query_embedding, chunks)

        # Then: returns 0.0
        self.assertEqual(score, 0.0)

    def test_get_document_context_for_chat(self):
        # Given: processed documents for a chat
        chat_id = "chat-123"
        processed_docs = [
            Document("doc-1", "guide.pdf", DocumentType.PDF, "/path1", chat_id, DocumentStatus.PROCESSED),
            Document("doc-2", "image.jpg", DocumentType.IMAGE, "/path2", chat_id, DocumentStatus.PROCESSED)
        ]
        
        self.document_service_mock.get_processed_documents_for_chat.return_value = processed_docs

        # When: getting document context
        result = self.rag_service.get_document_context_for_chat(chat_id)

        # Then: returns formatted document list
        expected = ["guide.pdf (pdf)", "image.jpg (image)"]
        self.assertEqual(result, expected)
        self.document_service_mock.get_processed_documents_for_chat.assert_called_once_with(chat_id)


if __name__ == '__main__':
    unittest.main() 