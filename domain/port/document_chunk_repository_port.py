from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.document_chunk import DocumentChunk


class DocumentChunkRepositoryPort(ABC):
    
    @abstractmethod
    def save_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Save multiple document chunks"""
        pass

    @abstractmethod
    def get_chunks_by_document_id(self, document_id: str) -> List[DocumentChunk]:
        """Get all chunks for a specific document"""
        pass

    @abstractmethod
    def get_chunk_by_id(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID"""
        pass

    @abstractmethod
    def delete_chunks_by_document_id(self, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        pass

    @abstractmethod
    def search_similar_chunks(
        self, 
        query_embedding: List[float], 
        chat_id: str,
        max_results: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[DocumentChunk]:
        """Search for similar chunks using vector similarity"""
        pass 