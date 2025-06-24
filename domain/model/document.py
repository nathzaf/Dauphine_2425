from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class DocumentType(Enum):
    PDF = "pdf"
    IMAGE = "image"


class DocumentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Document:
    def __init__(
        self,
        document_id: str,
        filename: str,
        document_type: DocumentType,
        file_path: str,
        chat_id: str,
        status: DocumentStatus = DocumentStatus.PENDING,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None
    ):
        self.document_id = document_id
        self.filename = filename
        self.document_type = document_type
        self.file_path = file_path
        self.chat_id = chat_id
        self.status = status
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now()

    def mark_as_processing(self):
        self.status = DocumentStatus.PROCESSING

    def mark_as_processed(self):
        self.status = DocumentStatus.PROCESSED

    def mark_as_failed(self):
        self.status = DocumentStatus.FAILED

    def is_processed(self) -> bool:
        return self.status == DocumentStatus.PROCESSED

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return self.document_id == other.document_id

    def __str__(self):
        return f"Document(id={self.document_id}, filename={self.filename}, type={self.document_type.value}, status={self.status.value})" 