from typing import List, Optional
from domain.model.document import Document, DocumentType, DocumentStatus
from domain.model.document_chunk import DocumentChunk
from domain.model.rag_query import RAGQuery, RAGResult
from domain.model.history import History
from domain.port.document_processor_port import DocumentProcessorPort
from domain.port.document_repository_port import DocumentRepositoryPort
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.embedding_service_port import EmbeddingServicePort
from domain.port.rag_generator_port import RAGGeneratorPort
from domain.port.generator_controller_port import GeneratorControllerPort


class RAGAdapter(GeneratorControllerPort):
    """RAG adapter implementing the generator controller interface with RAG capabilities."""
    
    def __init__(self,
                 document_processor: DocumentProcessorPort,
                 document_repository: DocumentRepositoryPort,
                 chunk_repository: DocumentChunkRepositoryPort,
                 embedding_service: EmbeddingServicePort,
                 rag_generator: RAGGeneratorPort):
        self.document_processor = document_processor
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service
        self.rag_generator = rag_generator
    
    def generate_message(self, prompt: str, chat_history: list) -> str:
        """Generate a message using RAG if relevant documents exist, otherwise fallback to normal generation."""
        # Convert chat_history to History object
        history = History(chat_id=self._extract_chat_id_from_history(chat_history))
        history.chat_history = chat_history
        
        # Try RAG approach first
        rag_result = self.query_with_rag(prompt, history.chat_id)
        
        if rag_result.has_relevant_context():
            # Use RAG generation with context
            return self.rag_generator.generate_response_with_context(
                query=prompt,
                context_chunks=rag_result.relevant_chunks,
                chat_history=history
            )
        else:
            # Fallback to normal generation without context
            return self.rag_generator.generate_response_without_context(
                query=prompt,
                chat_history=history
            )
    
    def save_history(self, history: History):
        """Save chat history - delegated to history repository if needed."""
        # This could be implemented if you have a history repository
        # For now, we'll pass as RAG doesn't directly handle history persistence
        pass
    
    def get_history(self, chat_id: str) -> History:
        """Get chat history - delegated to history repository if needed."""
        # This could be implemented if you have a history repository
        # For now, return empty history
        return History(chat_id=chat_id)
    
    def get_all_histories(self) -> list[History]:
        """Get all chat histories - delegated to history repository if needed."""
        # This could be implemented if you have a history repository
        return []
    
    # RAG-specific methods
    def add_document(self, file_path: str, filename: str, document_type: DocumentType, chat_id: str) -> Document:
        """Add a new document to the RAG system."""
        # Create document object
        document = Document(
            filename=filename,
            file_path=file_path,
            document_type=document_type,
            chat_id=chat_id,
            status=DocumentStatus.PROCESSING
        )
        
        # Save document
        saved_document = self.document_repository.save_document(document)
        
        try:
            # Process document to extract chunks
            chunks = self.document_processor.process_document(saved_document)
            
            # Save chunks with embeddings
            self.chunk_repository.save_chunks(chunks)
            
            # Update document status to processed
            self.document_repository.update_document_status(
                saved_document.document_id, 
                DocumentStatus.PROCESSED
            )
            
        except Exception as e:
            # Update document status to failed
            self.document_repository.update_document_status(
                saved_document.document_id, 
                DocumentStatus.FAILED
            )
            raise e
        
        return saved_document
    
    def query_with_rag(self, query: str, chat_id: str, max_chunks: int = 5, similarity_threshold: float = 0.7) -> RAGResult:
        """Query the RAG system and return results."""
        rag_query = RAGQuery(
            query=query,
            chat_id=chat_id,
            max_chunks=max_chunks,
            similarity_threshold=similarity_threshold
        )
        
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Search for similar chunks
        relevant_chunks = self.chunk_repository.search_similar_chunks(
            query_embedding=query_embedding,
            chat_id=chat_id,
            max_results=max_chunks,
            similarity_threshold=similarity_threshold
        )
        
        # For now, we'll generate the response in the calling method
        # This allows for better separation of concerns
        return RAGResult(
            query=rag_query,
            relevant_chunks=relevant_chunks,
            generated_response="",  # Will be generated by calling method
            confidence_score=self._calculate_confidence(relevant_chunks)
        )
    
    def remove_document(self, document_id: str) -> bool:
        """Remove a document and its chunks from the RAG system."""
        # Remove chunks first
        chunks_removed = self.chunk_repository.delete_chunks_by_document_id(document_id)
        
        # Remove document
        document_removed = self.document_repository.delete_document(document_id)
        
        return chunks_removed and document_removed
    
    def list_documents_for_chat(self, chat_id: str) -> List[Document]:
        """List all documents for a specific chat."""
        return self.document_repository.get_documents_by_chat_id(chat_id)
    
    def get_document_status(self, document_id: str) -> Optional[DocumentStatus]:
        """Get the processing status of a document."""
        document = self.document_repository.get_document_by_id(document_id)
        return document.status if document else None
    
    def _extract_chat_id_from_history(self, chat_history: list) -> str:
        """Extract chat ID from chat history. Implement based on your chat history structure."""
        # This is a placeholder - implement based on your actual chat history structure
        # You might have chat_id in the history or need to derive it differently
        return "default_chat"
    
    def _calculate_confidence(self, chunks: List[DocumentChunk]) -> float:
        """Calculate confidence score based on retrieved chunks."""
        if not chunks:
            return 0.0
        
        # Simple confidence calculation - can be improved
        # Based on number of chunks and their relevance
        base_confidence = min(len(chunks) / 5.0, 1.0)  # Normalize to max 5 chunks
        return base_confidence 