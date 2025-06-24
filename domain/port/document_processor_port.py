from abc import ABC, abstractmethod
from typing import List
from domain.model.document import Document
from domain.model.document_chunk import DocumentChunk


class DocumentProcessorPort(ABC):
    
    @abstractmethod
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from a PDF file"""
        pass

    @abstractmethod
    def extract_text_from_image(self, file_path: str) -> str:
        """Extract text content from an image using OCR"""
        pass

    @abstractmethod
    def split_text_into_chunks(
        self, 
        text: str, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200
    ) -> List[str]:
        """Split text into smaller chunks for processing"""
        pass

    @abstractmethod
    def process_document(self, document: Document) -> List[DocumentChunk]:
        """Process a document and return its chunks"""
        pass 