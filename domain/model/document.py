from typing import List, Dict, Any
from datetime import datetime

class Document:
    def __init__(self, 
                 document_id: str, 
                 title: str, 
                 content: str, 
                 document_type: str,
                 source_service: str = None,
                 metadata: Dict[str, Any] = None,
                 created_at: datetime = None):
        self.document_id = document_id
        self.title = title
        self.content = content
        self.document_type = document_type
        self.source_service = source_service or "unknown"
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "title": self.title,
            "content": self.content,
            "document_type": self.document_type,
            "source_service": self.source_service,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }

class DocumentChunk:
    def __init__(self, 
                 chunk_id: str,
                 document_id: str,
                 content: str,
                 chunk_index: int,
                 metadata: Dict[str, Any] = None):
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.content = content
        self.chunk_index = chunk_index
        self.metadata = metadata or {} 