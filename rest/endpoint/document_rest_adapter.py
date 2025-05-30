from http import HTTPStatus
from typing import List
from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel

from domain.service.document_service import DocumentService

class DocumentUploadRequest(BaseModel):
    title: str
    content: str
    document_type: str
    source_service: str = "manual_upload"

class DocumentResponse(BaseModel):
    document_id: str
    title: str
    document_type: str
    source_service: str
    created_at: str

class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = 5

class DocumentRestAdapter:
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    async def upload_document(self, request: DocumentUploadRequest) -> DocumentResponse:
        try:
            document_id = self.document_service.process_document(
                title=request.title,
                content=request.content,
                document_type=request.document_type,
                source_service=request.source_service
            )
            
            document = self.document_service.get_document_by_id(document_id)
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
            chunks = self.document_service.search_relevant_documents(
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

    async def get_documents_by_type(self, document_type: str):
        try:
            documents = self.document_service.get_documents_by_type(document_type)
            return {
                "document_type": document_type,
                "documents": [
                    {
                        "document_id": doc.document_id,
                        "title": doc.title,
                        "document_type": doc.document_type,
                        "source_service": doc.source_service,
                        "created_at": doc.created_at.isoformat()
                    }
                    for doc in documents
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/documents")(self.upload_document)
        router.post("/documents/search")(self.search_documents)
        router.get("/documents/type/{document_type}")(self.get_documents_by_type)
        return router 