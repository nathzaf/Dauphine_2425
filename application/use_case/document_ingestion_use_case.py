from typing import List, Dict, Any
from domain.service.document_service import DocumentService
from domain.port.document_ingestion_port import DocumentIngestionPort

class DocumentIngestionUseCase:
    def __init__(self, document_service: DocumentService, 
                 document_ingestion_adapter: DocumentIngestionPort):
        self.document_service = document_service
        self.document_ingestion_adapter = document_ingestion_adapter

    def ingest_user_documents(self, user_id: str, user_info: Dict[str, Any]) -> List[str]:
        """Ingest documents for a specific user"""
        return self.document_ingestion_adapter.ingest_user_specific_documents(user_id, user_info)

    def ingest_from_external_source(self, source_id: str, source_config: Dict[str, Any]) -> List[str]:
        """Ingest documents from external sources"""
        return self.document_ingestion_adapter.ingest_from_external_source(source_id, source_config) 