import json
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from domain.model.document import Document, DocumentChunk
from domain.port.document_repository_port import DocumentRepositoryPort

class DocumentRepositoryAdapter(DocumentRepositoryPort):
    def __init__(self):
        self.documents_path = './data/documents.json'
        self.chunks_path = './data/document_chunks.json'
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Create empty files if they don't exist"""
        for path in [self.documents_path, self.chunks_path]:
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as file:
                    json.dump([], file)

    def save_document(self, document: Document) -> str:
        """Save a document and return its ID"""
        with open(self.documents_path, 'r+') as file:
            documents = json.load(file)
            
            # Check if document already exists
            for i, doc in enumerate(documents):
                if doc.get("document_id") == document.document_id:
                    documents[i] = document.to_dict()
                    break
            else:
                documents.append(document.to_dict())
            
            file.seek(0)
            json.dump(documents, file, indent=2)
            file.truncate()
        
        return document.document_id

    def get_document(self, document_id: str) -> Optional[Document]:
        """Retrieve a document by ID"""
        with open(self.documents_path, 'r') as file:
            documents = json.load(file)
            
        for doc_data in documents:
            if doc_data.get("document_id") == document_id:
                return Document(
                    document_id=doc_data["document_id"],
                    title=doc_data["title"],
                    content=doc_data["content"],
                    document_type=doc_data["document_type"],
                    source_service=doc_data.get("source_service"),
                    metadata=doc_data.get("metadata", {}),
                    created_at=datetime.fromisoformat(doc_data["created_at"])
                )
        
        return None

    def get_documents_by_type(self, document_type: str) -> List[Document]:
        """Get all documents of a specific type"""
        with open(self.documents_path, 'r') as file:
            documents = json.load(file)
            
        result = []
        for doc_data in documents:
            if doc_data.get("document_type") == document_type:
                result.append(Document(
                    document_id=doc_data["document_id"],
                    title=doc_data["title"],
                    content=doc_data["content"],
                    document_type=doc_data["document_type"],
                    source_service=doc_data.get("source_service"),
                    metadata=doc_data.get("metadata", {}),
                    created_at=datetime.fromisoformat(doc_data["created_at"])
                ))
        return result

    def get_all_documents(self) -> List[Document]:
        """Get all documents"""
        with open(self.documents_path, 'r') as file:
            documents = json.load(file)
            
        result = []
        for doc_data in documents:
            result.append(Document(
                document_id=doc_data["document_id"],
                title=doc_data["title"],
                content=doc_data["content"],
                document_type=doc_data["document_type"],
                source_service=doc_data.get("source_service"),
                metadata=doc_data.get("metadata", {}),
                created_at=datetime.fromisoformat(doc_data["created_at"])
            ))
        return result

    def save_chunks(self, chunks: List[DocumentChunk]):
        """Save document chunks for search"""
        with open(self.chunks_path, 'r+') as file:
            existing_chunks = json.load(file)
            
            # Remove existing chunks for the same document
            if chunks:
                document_id = chunks[0].document_id
                existing_chunks = [c for c in existing_chunks if c.get("document_id") != document_id]
            
            # Add new chunks
            for chunk in chunks:
                existing_chunks.append({
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "metadata": chunk.metadata
                })
            
            file.seek(0)
            json.dump(existing_chunks, file, indent=2)
            file.truncate()

    def search_chunks(self, query: str, limit: int = 5) -> List[DocumentChunk]:
        """Simple text-based search through chunks"""
        with open(self.chunks_path, 'r') as file:
            chunks_data = json.load(file)
        
        # Simple keyword matching (can be enhanced with vector search)
        query_words = query.lower().split()
        scored_chunks = []
        
        for chunk_data in chunks_data:
            content = chunk_data["content"].lower()
            score = sum(1 for word in query_words if word in content)
            
            if score > 0:
                scored_chunks.append((score, DocumentChunk(
                    chunk_id=chunk_data["chunk_id"],
                    document_id=chunk_data["document_id"],
                    content=chunk_data["content"],
                    chunk_index=chunk_data["chunk_index"],
                    metadata=chunk_data.get("metadata", {})
                )))
        
        # Sort by score and return top results
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:limit]] 