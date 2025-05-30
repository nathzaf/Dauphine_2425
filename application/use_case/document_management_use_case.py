from typing import List, Dict, Any, Optional
from domain.service.document_service import DocumentService
from domain.model.document import Document, DocumentChunk

class DocumentManagementUseCase:
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    def upload_document(self, title: str, content: str, document_type: str, 
                       source_service: str = "manual_upload", 
                       metadata: Dict[str, Any] = None) -> str:
        """Upload and process a new document"""
        return self.document_service.process_document_with_chunks(
            title=title,
            content=content,
            document_type=document_type,
            source_service=source_service,
            metadata=metadata
        )

    def search_documents(self, query: str, limit: int = 5) -> List[DocumentChunk]:
        """Search through documents"""
        return self.document_service.search_relevant_content(query, limit)

    def get_document(self, document_id: str) -> Optional[Document]:
        """Get a specific document"""
        return self.document_service.get_document_by_id(document_id)

    def get_documents_by_type(self, document_type: str) -> List[Document]:
        """Get documents by type"""
        return self.document_service.get_documents_by_type(document_type) 