import os
from typing import List
import cohere
import numpy as np
from dotenv import load_dotenv
from domain.port.embedding_service_port import EmbeddingServicePort

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')


class CohereEmbeddingService(EmbeddingServicePort):
    """Cohere implementation for embedding generation and similarity calculation."""
    
    def __init__(self, model_name: str = "embed-english-v3.0"):
        self.client = cohere.Client(COHERE_API_KEY)
        self.model_name = model_name
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for a text."""
        response = self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type="search_document"
        )
        return response.embeddings[0]
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            return []
        
        response = self.client.embed(
            texts=texts,
            model=self.model_name,
            input_type="search_document"
        )
        return response.embeddings
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        a = np.array(embedding1)
        b = np.array(embedding2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))) 