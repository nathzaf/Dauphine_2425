from pydantic import BaseModel

class DocumentResponse(BaseModel):
    document_id: str
    title: str
    document_type: str
    source_service: str
    created_at: str 