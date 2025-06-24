from typing import List, Optional
from domain.model.document import Document, DocumentStatus
from domain.port.document_repository_port import DocumentRepositoryPort


class InMemoryDocumentRepository(DocumentRepositoryPort):
    """In-memory implementation of document repository."""
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def save_document(self, document: Document) -> Document:
        """Save a document to the repository."""
        # Check if document already exists and update it
        for i, existing_doc in enumerate(self.documents):
            if existing_doc.document_id == document.document_id:
                self.documents[i] = document
                return document
        
        # Add new document
        self.documents.append(document)
        return document
    
    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        """Retrieve a document by its ID."""
        for document in self.documents:
            if document.document_id == document_id:
                return document
        return None
    
    def get_documents_by_chat_id(self, chat_id: str) -> List[Document]:
        """Get all documents for a specific chat."""
        return [doc for doc in self.documents if doc.chat_id == chat_id]
    
    def get_documents_by_status(self, status: DocumentStatus) -> List[Document]:
        """Get all documents with a specific status."""
        return [doc for doc in self.documents if doc.status == status]
    
    def update_document_status(self, document_id: str, status: DocumentStatus) -> bool:
        """Update the status of a document."""
        for document in self.documents:
            if document.document_id == document_id:
                document.status = status
                return True
        return False
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the repository."""
        for i, document in enumerate(self.documents):
            if document.document_id == document_id:
                del self.documents[i]
                return True
        return False 