from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.document import Document, DocumentStatus


class DocumentRepositoryPort(ABC):
    
    @abstractmethod
    def save_document(self, document: Document) -> Document:
        """Save a document to the repository"""
        pass

    @abstractmethod
    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        """Retrieve a document by its ID"""
        pass

    @abstractmethod
    def get_documents_by_chat_id(self, chat_id: str) -> List[Document]:
        """Get all documents for a specific chat"""
        pass

    @abstractmethod
    def get_documents_by_status(self, status: DocumentStatus) -> List[Document]:
        """Get all documents with a specific status"""
        pass

    @abstractmethod
    def update_document_status(self, document_id: str, status: DocumentStatus) -> bool:
        """Update the status of a document"""
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the repository"""
        pass 