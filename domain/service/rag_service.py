from typing import List, Optional
from domain.model.rag_query import RAGQuery, RAGResult
from domain.model.document_chunk import DocumentChunk
from domain.model.history import History
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.embedding_service_port import EmbeddingServicePort
from domain.port.rag_generator_port import RAGGeneratorPort
from domain.service.document_service import DocumentService


class RAGService:
    def __init__(
        self,
        chunk_repository: DocumentChunkRepositoryPort,
        embedding_service: EmbeddingServicePort,
        rag_generator: RAGGeneratorPort,
        document_service: DocumentService
    ):
        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service
        self.rag_generator = rag_generator
        self.document_service = document_service

    def query_with_rag(
        self,
        query: str,
        chat_id: str,
        chat_history: History,
        max_chunks: int = 5,
        similarity_threshold: float = 0.7
    ) -> RAGResult:
        """Perform RAG query and generate response"""
        rag_query = RAGQuery(
            query=query,
            chat_id=chat_id,
            max_chunks=max_chunks,
            similarity_threshold=similarity_threshold
        )

        # Check if there are processed documents for this chat
        processed_docs = self.document_service.get_processed_documents_for_chat(chat_id)
        
        if not processed_docs:
            # No documents available, use fallback generation
            response = self.rag_generator.generate_response_without_context(
                query, chat_history
            )
            return RAGResult(
                query=rag_query,
                relevant_chunks=[],
                generated_response=response,
                confidence_score=0.0
            )

        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)

        # Search for similar chunks
        relevant_chunks = self.chunk_repository.search_similar_chunks(
            query_embedding=query_embedding,
            chat_id=chat_id,
            max_results=max_chunks,
            similarity_threshold=similarity_threshold
        )

        if not relevant_chunks:
            # No relevant context found, use fallback
            response = self.rag_generator.generate_response_without_context(
                query, chat_history
            )
            confidence_score = 0.0
        else:
            # Generate response with context
            response = self.rag_generator.generate_response_with_context(
                query, relevant_chunks, chat_history
            )
            # Calculate average similarity as confidence score
            confidence_score = self._calculate_confidence_score(
                query_embedding, relevant_chunks
            )

        return RAGResult(
            query=rag_query,
            relevant_chunks=relevant_chunks,
            generated_response=response,
            confidence_score=confidence_score
        )

    def _calculate_confidence_score(
        self, 
        query_embedding: List[float], 
        chunks: List[DocumentChunk]
    ) -> float:
        """Calculate confidence score based on similarity scores"""
        if not chunks:
            return 0.0

        similarities = []
        for chunk in chunks:
            if chunk.has_embedding():
                similarity = self.embedding_service.calculate_similarity(
                    query_embedding, chunk.embedding
                )
                similarities.append(similarity)

        return sum(similarities) / len(similarities) if similarities else 0.0

    def get_document_context_for_chat(self, chat_id: str) -> List[str]:
        """Get a summary of available documents for a chat"""
        documents = self.document_service.get_processed_documents_for_chat(chat_id)
        return [f"{doc.filename} ({doc.document_type.value})" for doc in documents] 