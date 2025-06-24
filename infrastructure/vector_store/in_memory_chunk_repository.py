from typing import List, Optional
import numpy as np
from domain.model.document_chunk import DocumentChunk
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort
from domain.port.embedding_service_port import EmbeddingServicePort


class InMemoryChunkRepository(DocumentChunkRepositoryPort):
    """In-memory implementation of document chunk repository with vector search."""
    
    def __init__(self, embedding_service: EmbeddingServicePort):
        self.chunks: List[DocumentChunk] = []
        self.embeddings: List[List[float]] = []
        self.embedding_service = embedding_service
    
    def save_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Save multiple document chunks and generate their embeddings."""
        if not chunks:
            return []
        
        # Generate embeddings for all chunks
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedding_service.generate_embeddings_batch(texts)
        
        # Store chunks and embeddings
        for chunk, embedding in zip(chunks, embeddings):
            self.chunks.append(chunk)
            self.embeddings.append(embedding)
        
        return chunks
    
    def get_chunks_by_document_id(self, document_id: str) -> List[DocumentChunk]:
        """Get all chunks for a specific document."""
        return [chunk for chunk in self.chunks if chunk.document_id == document_id]
    
    def get_chunk_by_id(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID."""
        for chunk in self.chunks:
            if chunk.chunk_id == chunk_id:
                return chunk
        return None
    
    def delete_chunks_by_document_id(self, document_id: str) -> bool:
        """Delete all chunks for a specific document."""
        indices_to_remove = []
        for i, chunk in enumerate(self.chunks):
            if chunk.document_id == document_id:
                indices_to_remove.append(i)
        
        # Remove in reverse order to maintain indices
        for i in reversed(indices_to_remove):
            del self.chunks[i]
            del self.embeddings[i]
        
        return len(indices_to_remove) > 0
    
    def search_similar_chunks(
        self, 
        query_embedding: List[float], 
        chat_id: str,
        max_results: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[DocumentChunk]:
        """Search for similar chunks using vector similarity."""
        if not self.chunks:
            return []
        
        # Filter chunks by chat_id and calculate similarities
        similarities = []
        for i, (chunk, embedding) in enumerate(zip(self.chunks, self.embeddings)):
            if chunk.chat_id == chat_id:
                similarity = self.embedding_service.calculate_similarity(query_embedding, embedding)
                if similarity >= similarity_threshold:
                    similarities.append((i, similarity))
        
        # Sort by similarity (descending) and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:max_results]]
        
        return [self.chunks[i] for i in top_indices] 