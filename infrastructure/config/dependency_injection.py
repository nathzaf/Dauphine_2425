from domain.service.document_service import DocumentService
from domain.service.rag_service import RAGService
from domain.service.history_service import HistoryService
from application.use_case.chat_use_case import ChatUseCase
from application.use_case.document_management_use_case import DocumentManagementUseCase
from application.use_case.document_ingestion_use_case import DocumentIngestionUseCase

from infrastructure.adapter.document_repository_adapter import DocumentRepositoryAdapter
from infrastructure.adapter.cohere_text_generator_adapter import CohereTextGeneratorAdapter
from infrastructure.adapter.document_ingestion_adapter import DocumentIngestionAdapter
from infrastructure.adapter.chat_application_adapter import ChatApplicationAdapter
from infrastructure.history_repository.history_repository import HistoryRepository

from rest.controller.chat_controller import ChatController
from rest.controller.document_controller import DocumentController

class DependencyContainer:
    def __init__(self):
        # Infrastructure adapters
        self.document_repository = DocumentRepositoryAdapter()
        self.text_generator = CohereTextGeneratorAdapter()
        self.history_repository = HistoryRepository()
        
        # Domain services
        self.document_service = DocumentService(self.document_repository)
        self.rag_service = RAGService(self.document_service, self.text_generator)
        
        # Chat application adapter for history
        self.chat_application_adapter = ChatApplicationAdapter(
            text_generator=None,  # Not needed since we use RAG service directly
            history_repository=self.history_repository
        )
        self.history_service = HistoryService(self.chat_application_adapter)
        
        # Document ingestion
        self.document_ingestion_adapter = DocumentIngestionAdapter(self.document_service)
        
        # Application use cases
        self.chat_use_case = ChatUseCase(self.rag_service, self.history_service)
        self.document_management_use_case = DocumentManagementUseCase(self.document_service)
        self.document_ingestion_use_case = DocumentIngestionUseCase(
            self.document_service, 
            self.document_ingestion_adapter
        )
        
        # REST controllers
        self.chat_controller = ChatController(self.chat_use_case)
        self.document_controller = DocumentController(
            self.document_management_use_case,
            self.document_ingestion_use_case
        )

# Global container instance
container = DependencyContainer() 