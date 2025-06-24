from abc import ABC, abstractmethod
from typing import List
from domain.model.document_chunk import DocumentChunk
from domain.model.history import History


class RAGGeneratorPort(ABC):
    
    @abstractmethod
    def generate_response_with_context(
        self,
        query: str,
        context_chunks: List[DocumentChunk],
        chat_history: History
    ) -> str:
        """Generate a response using the provided context chunks and chat history"""
        pass

    @abstractmethod
    def generate_response_without_context(
        self,
        query: str,
        chat_history: History
    ) -> str:
        """Generate a response without RAG context (fallback)"""
        pass 