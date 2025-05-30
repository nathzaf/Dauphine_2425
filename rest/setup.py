from domain.adapter.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.history_service import HistoryService
from domain.service.text_generation_service import TextGenerationService
from domain.service.document_service import DocumentService
from infrastructure.adapter.rag_chat_application_adapter import RAGChatApplicationAdapter
from infrastructure.history_repository.history_repository import HistoryRepository
from infrastructure.document_repository.document_repository import DocumentRepository
from infrastructure.text_generator.rag_cohere_text_generator import RAGCohereTextGenerator

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter
from rest.endpoint.document_rest_adapter import DocumentRestAdapter

def create_generator_rest_adapter():
    # Document components
    document_repository = DocumentRepository()
    document_service = DocumentService(document_repository)
    
    # Chat components with RAG
    text_generator = RAGCohereTextGenerator(document_service)
    history_repository = HistoryRepository()
    chat_application_adapter = RAGChatApplicationAdapter(
        text_generator=text_generator,
        history_repository=history_repository
    )
    
    history_service = HistoryService(chat_application_adapter)
    text_generation_service = TextGenerationService(chat_application_adapter)
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service, history_service)
    
    return GeneratorRestAdapter(generator_controller_adapter)

def create_document_rest_adapter():
    document_repository = DocumentRepository()
    document_service = DocumentService(document_repository)
    return DocumentRestAdapter(document_service)
