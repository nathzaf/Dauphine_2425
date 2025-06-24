from typing import List, Optional
from domain.model.document_chunk import DocumentChunk


class RAGQuery:
    def __init__(
        self,
        query: str,
        chat_id: str,
        max_chunks: int = 5,
        similarity_threshold: float = 0.7
    ):
        self.query = query
        self.chat_id = chat_id
        self.max_chunks = max_chunks
        self.similarity_threshold = similarity_threshold

    def __str__(self):
        return f"RAGQuery(query='{self.query[:50]}...', chat_id={self.chat_id})"


class RAGResult:
    def __init__(
        self,
        query: RAGQuery,
        relevant_chunks: List[DocumentChunk],
        generated_response: str,
        confidence_score: Optional[float] = None
    ):
        self.query = query
        self.relevant_chunks = relevant_chunks
        self.generated_response = generated_response
        self.confidence_score = confidence_score

    def has_relevant_context(self) -> bool:
        return len(self.relevant_chunks) > 0

    def get_source_documents(self) -> List[str]:
        """Returns unique document IDs that contributed to the response"""
        return list(set(chunk.document_id for chunk in self.relevant_chunks))

    def __str__(self):
        return f"RAGResult(chunks={len(self.relevant_chunks)}, confidence={self.confidence_score})" 