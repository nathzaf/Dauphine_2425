from pydantic import BaseModel, Field
from typing import Dict, Any

class DocumentUploadRequest(BaseModel):
    title: str
    content: str
    document_type: str
    source_service: str = "manual_upload"
    metadata: Dict[str, Any] = {}

class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = 5

class UserDocumentIngestionRequest(BaseModel):
    user_id: str
    user_info: Dict[str, Any] 