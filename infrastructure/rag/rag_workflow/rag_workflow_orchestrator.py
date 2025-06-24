import os
from typing import List
import cohere
from dotenv import load_dotenv
from domain.model.document_chunk import DocumentChunk
from domain.port.embedding_service_port import EmbeddingServicePort
from domain.port.document_chunk_repository_port import DocumentChunkRepositoryPort

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')


class RAGWorkflowOrchestrator:
    """Orchestrates the RAG workflow: rephrase -> retrieve -> filter."""
    
    def __init__(self, 
                 embedding_service: EmbeddingServicePort,
                 chunk_repository: DocumentChunkRepositoryPort,
                 model_name: str = "command-r-plus"):
        self.embedding_service = embedding_service
        self.chunk_repository = chunk_repository
        self.client = cohere.Client(COHERE_API_KEY)
        self.model_name = model_name
        
        self.rephrase_prompt = """
        You are an expert at optimizing search queries. Your task is to rephrase the user's question 
        to make it more effective for semantic search in a document database.
        
        Guidelines:
        - Keep the core meaning intact
        - Use more specific and descriptive terms
        - Remove conversational elements
        - Focus on key concepts and entities
        
        Original question: {question}
        
        Rephrased question:"""
        
        self.filter_prompt = """
        You are a document relevance evaluator. Determine if the given document chunk is relevant 
        to answering the user's question.
        
        Question: {question}
        
        Document chunk: {chunk}
        
        Is this document chunk relevant to answering the question? Respond with only "YES" or "NO".
        
        Answer:"""
    
    def process_query(self, question: str, chat_id: str, max_results: int = 5) -> List[DocumentChunk]:
        """Process a query through the complete RAG workflow."""
        # Step 1: Rephrase the question for better retrieval
        rephrased_question = self._rephrase_question(question)
        
        # Step 2: Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(rephrased_question)
        
        # Step 3: Retrieve similar chunks
        retrieved_chunks = self.chunk_repository.search_similar_chunks(
            query_embedding=query_embedding,
            chat_id=chat_id,
            max_results=max_results * 2,  # Get more to filter later
            similarity_threshold=0.3
        )
        
        # Step 4: Filter chunks for relevance
        filtered_chunks = self._filter_relevant_chunks(question, retrieved_chunks)
        
        # Return top results
        return filtered_chunks[:max_results]
    
    def _rephrase_question(self, question: str) -> str:
        """Rephrase the question for better semantic search."""
        try:
            response = self.client.chat(
                model=self.model_name,
                message=self.rephrase_prompt.format(question=question),
                temperature=0.3
            )
            return response.text.strip()
        except Exception as e:
            print(f"Question rephrasing failed: {e}")
            return question
    
    def _filter_relevant_chunks(self, question: str, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Filter chunks based on relevance to the question."""
        if not chunks:
            return []
        
        relevant_chunks = []
        
        for chunk in chunks:
            try:
                response = self.client.chat(
                    model=self.model_name,
                    message=self.filter_prompt.format(question=question, chunk=chunk.content),
                    temperature=0.1
                )
                
                if response.text.strip().upper() == "YES":
                    relevant_chunks.append(chunk)
                    
            except Exception as e:
                print(f"Chunk filtering failed: {e}")
                # Include chunk if filtering fails (conservative approach)
                relevant_chunks.append(chunk)
        
        return relevant_chunks 