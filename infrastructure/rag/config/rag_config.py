import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RAGConfig:
    """Configuration for RAG system."""
    
    # Cohere API settings
    cohere_api_key: str = os.environ.get('COHERE_API_KEY', '')
    embedding_model: str = "embed-english-v3.0"
    chat_model: str = "command-r-plus"
    
    # Document processing settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Vector search settings
    similarity_threshold: float = 0.3
    max_chunks_per_query: int = 5
    
    # Generation settings
    temperature: float = 0.7
    max_tokens: int = 1000
    
    def validate(self) -> bool:
        """Validate the configuration."""
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        return True


# Global config instance
rag_config = RAGConfig() 