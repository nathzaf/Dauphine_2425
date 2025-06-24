from infrastructure.rag.document_processor.document_processor import DocumentProcessor
from infrastructure.rag.embedding_service.cohere_embedding_service import CohereEmbeddingService
from infrastructure.rag.rag_generator.cohere_rag_generator import CohereRAGGenerator
from infrastructure.vector_store.in_memory_chunk_repository import InMemoryChunkRepository
from infrastructure.rag.document_repository.in_memory_document_repository import InMemoryDocumentRepository
from infrastructure.rag.rag_workflow.rag_workflow_orchestrator import RAGWorkflowOrchestrator
from infrastructure.rag.config.rag_config import rag_config


class RAGFactory:
    """Factory for creating RAG system components using the correct ports."""
    
    @staticmethod
    def create_document_processor() -> DocumentProcessor:
        """Create a document processor."""
        return DocumentProcessor(
            chunk_size=rag_config.chunk_size,
            chunk_overlap=rag_config.chunk_overlap
        )
    
    @staticmethod
    def create_embedding_service() -> CohereEmbeddingService:
        """Create an embedding service."""
        return CohereEmbeddingService(model_name=rag_config.embedding_model)
    
    @staticmethod
    def create_rag_generator() -> CohereRAGGenerator:
        """Create a RAG generator."""
        return CohereRAGGenerator(model_name=rag_config.chat_model)
    
    @staticmethod
    def create_chunk_repository(embedding_service: CohereEmbeddingService) -> InMemoryChunkRepository:
        """Create a chunk repository with vector search capabilities."""
        return InMemoryChunkRepository(embedding_service=embedding_service)
    
    @staticmethod
    def create_document_repository() -> InMemoryDocumentRepository:
        """Create a document repository."""
        return InMemoryDocumentRepository()
    
    @staticmethod
    def create_rag_workflow_orchestrator(
        embedding_service: CohereEmbeddingService,
        chunk_repository: InMemoryChunkRepository
    ) -> RAGWorkflowOrchestrator:
        """Create a RAG workflow orchestrator."""
        return RAGWorkflowOrchestrator(
            embedding_service=embedding_service,
            chunk_repository=chunk_repository,
            model_name=rag_config.chat_model
        )
    
    @staticmethod
    def create_complete_rag_system():
        """Create a complete RAG system with all components."""
        rag_config.validate()
        
        embedding_service = RAGFactory.create_embedding_service()
        chunk_repository = RAGFactory.create_chunk_repository(embedding_service)
        document_repository = RAGFactory.create_document_repository()
        document_processor = RAGFactory.create_document_processor()
        rag_generator = RAGFactory.create_rag_generator()
        workflow_orchestrator = RAGFactory.create_rag_workflow_orchestrator(
            embedding_service, chunk_repository
        )
        
        return {
            'embedding_service': embedding_service,
            'chunk_repository': chunk_repository,
            'document_repository': document_repository,
            'document_processor': document_processor,
            'rag_generator': rag_generator,
            'workflow_orchestrator': workflow_orchestrator
        } 