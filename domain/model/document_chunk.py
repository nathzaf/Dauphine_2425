from typing import Optional, Dict, Any


class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        document_id: str,
        content: str,
        chunk_index: int,
        embedding: Optional[list[float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.content = content
        self.chunk_index = chunk_index
        self.embedding = embedding
        self.metadata = metadata or {}

    def has_embedding(self) -> bool:
        return self.embedding is not None and len(self.embedding) > 0

    def __eq__(self, other):
        if not isinstance(other, DocumentChunk):
            return False
        return self.chunk_id == other.chunk_id

    def __str__(self):
        return f"DocumentChunk(id={self.chunk_id}, doc_id={self.document_id}, index={self.chunk_index})" 