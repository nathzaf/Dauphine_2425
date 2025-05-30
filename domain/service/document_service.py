import uuid
from typing import List, Dict, Any, Optional
from domain.model.document import Document, DocumentChunk
from domain.port.document_repository_port import DocumentRepositoryPort

class DocumentService:
    def __init__(self, document_repository: DocumentRepositoryPort):
        self.document_repository = document_repository

    def create_document(self, title: str, content: str, document_type: str, 
                       source_service: str = None, metadata: Dict[str, Any] = None) -> str:
        """Create and store a new document"""
        document_id = str(uuid.uuid4())
        
        document = Document(
            document_id=document_id,
            title=title,
            content=content,
            document_type=document_type,
            source_service=source_service,
            metadata=metadata
        )
        
        return self.document_repository.save_document(document)

    def process_document_with_chunks(self, title: str, content: str, document_type: str, 
                                   source_service: str = None, metadata: Dict[str, Any] = None) -> str:
        """Process and store a document with chunks for search optimization"""
        document_id = self.create_document(title, content, document_type, source_service, metadata)
        
        # Get the document to create chunks
        document = self.document_repository.get_document(document_id)
        if document:
            chunks = self._create_chunks(document)
            self.document_repository.save_chunks(chunks)
        
        return document_id

    def search_relevant_content(self, query: str, limit: int = 3) -> List[DocumentChunk]:
        """Search for relevant document chunks"""
        return self.document_repository.search_chunks(query, limit)

    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        """Retrieve a specific document"""
        return self.document_repository.get_document(document_id)

    def get_documents_by_type(self, document_type: str) -> List[Document]:
        """Get documents by type"""
        return self.document_repository.get_documents_by_type(document_type)

    def _create_chunks(self, document: Document, chunk_size: int = 500) -> List[DocumentChunk]:
        """Split document into searchable chunks"""
        content = document.content
        chunks = []
        
        for i in range(0, len(content), chunk_size):
            chunk_content = content[i:i + chunk_size]
            
            # Try to break at word boundaries
            if i + chunk_size < len(content):
                last_space = chunk_content.rfind(' ')
                if last_space > chunk_size * 0.8:
                    chunk_content = chunk_content[:last_space]
            
            chunk = DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                document_id=document.document_id,
                content=chunk_content.strip(),
                chunk_index=i // chunk_size,
                metadata={"original_title": document.title, "document_type": document.document_type}
            )
            chunks.append(chunk)
        
        return chunks 