import os
import io
from typing import List
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from domain.model.document import Document
from domain.model.document_chunk import DocumentChunk
from domain.port.document_processor_port import DocumentProcessorPort


class DocumentProcessor(DocumentProcessorPort):
    """Infrastructure implementation for document processing using PyMuPDF and Tesseract."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        doc = fitz.open(file_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
        return text.strip()
    
    def extract_text_from_image(self, file_path: str) -> str:
        """Extract text from image using Tesseract OCR."""
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into chunks for better retrieval."""
        # Use provided parameters or fall back to instance defaults
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size or self.chunk_size,
            chunk_overlap=chunk_overlap or self.chunk_overlap,
            length_function=len,
        )
        return splitter.split_text(text)
    
    def process_document(self, document: Document) -> List[DocumentChunk]:
        """Process a document and return its chunks."""
        # Extract text based on document type
        if document.document_type.value == "pdf":
            # Assuming document.file_path exists or we need to save the content first
            text = self.extract_text_from_pdf(document.file_path)
        elif document.document_type.value == "image":
            text = self.extract_text_from_image(document.file_path)
        else:
            raise ValueError(f"Unsupported document type: {document.document_type}")
        
        # Split into chunks
        text_chunks = self.split_text_into_chunks(text)
        
        # Create DocumentChunk objects
        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            chunk = DocumentChunk(
                content=chunk_text,
                chunk_index=i,
                document_id=document.document_id,
                chat_id=document.chat_id
            )
            chunks.append(chunk)
        
        return chunks 