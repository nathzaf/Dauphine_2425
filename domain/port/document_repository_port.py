from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.document import Document, DocumentChunk

class DocumentRepositoryPort(ABC):
    
    @abstractmethod
    def save_document(self, document: Document) -> str:
        pass
    
    @abstractmethod
    def get_document(self, document_id: str) -> Optional[Document]:
        pass
    
    @abstractmethod
    def get_documents_by_type(self, document_type: str) -> List[Document]:
        pass
    
    @abstractmethod
    def get_all_documents(self) -> List[Document]:
        pass
    
    @abstractmethod
    def save_chunks(self, chunks: List[DocumentChunk]):
        pass
    
    @abstractmethod
    def search_chunks(self, query: str, limit: int = 5) -> List[DocumentChunk]:
        pass 