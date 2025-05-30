from fastapi import APIRouter, HTTPException
from typing import List
from application.use_case.document_management_use_case import DocumentManagementUseCase
from application.use_case.document_ingestion_use_case import DocumentIngestionUseCase
from rest.model.document_request import DocumentUploadRequest, DocumentSearchRequest
from rest.model.document_response import DocumentResponse

class DocumentController:
    def __init__(self, document_management_use_case: DocumentManagementUseCase,
                 document_ingestion_use_case: DocumentIngestionUseCase):
        self.document_management_use_case = document_management_use_case
        self.document_ingestion_use_case = document_ingestion_use_case

    async def upload_document(self, request: DocumentUploadRequest) -> DocumentResponse:
        try:
            document_id = self.document_management_use_case.upload_document(
                title=request.title,
                content=request.content,
                document_type=request.document_type,
                source_service=request.source_service
            )
            
            document = self.document_management_use_case.get_document(document_id)
            return DocumentResponse(
                document_id=document.document_id,
                title=document.title,
                document_type=document.document_type,
                source_service=document.source_service,
                created_at=document.created_at.isoformat()
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def search_documents(self, request: DocumentSearchRequest):
        try:
            chunks = self.document_management_use_case.search_documents(
                query=request.query,
                limit=request.limit
            )
            
            return {
                "query": request.query,
                "results": [
                    {
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "metadata": chunk.metadata
                    }
                    for chunk in chunks
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def ingest_user_documents(self, user_id: str, user_info: dict):
        try:
            document_ids = self.document_ingestion_use_case.ingest_user_documents(user_id, user_info)
            return {
                "status": "success",
                "message": f"Ingested {len(document_ids)} documents",
                "document_ids": document_ids,
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/documents")(self.upload_document)
        router.post("/documents/search")(self.search_documents)
        router.post("/documents/ingest")(self.ingest_user_documents)
        return router 