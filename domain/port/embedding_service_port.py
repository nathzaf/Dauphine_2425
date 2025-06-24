from abc import ABC, abstractmethod
from typing import List


class EmbeddingServicePort(ABC):
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for a text"""
        pass

    @abstractmethod
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        pass

    @abstractmethod
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate similarity score between two embeddings"""
        pass 