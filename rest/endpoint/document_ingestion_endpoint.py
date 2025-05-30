from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from infrastructure.service.document_ingestion_service import DocumentIngestionService
from domain.service.document_service import DocumentService
from infrastructure.document_repository.document_repository import DocumentRepository

class UserDocumentIngestionRequest(BaseModel):
    user_id: str
    user_info: Dict[str, Any]

class DocumentIngestionRestAdapter:
    def __init__(self):
        document_repository = DocumentRepository()
        document_service = DocumentService(document_repository)
        self.ingestion_service = DocumentIngestionService(document_service)

    async def ingest_user_documents(self, request: UserDocumentIngestionRequest):
        try:
            document_ids = self.ingestion_service.ingest_caf_documents(
                user_id=request.user_id,
                user_info=request.user_info
            )
            
            return {
                "status": "success",
                "message": f"Ingested {len(document_ids)} documents",
                "document_ids": document_ids,
                "user_id": request.user_id
            }
        except Exception as e:
            print(f"Error in document ingestion: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/documents/ingest")(self.ingest_user_documents)
        return router 