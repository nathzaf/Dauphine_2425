import os
from typing import List
import cohere
from dotenv import load_dotenv
from domain.model.document_chunk import DocumentChunk
from domain.model.history import History
from domain.port.rag_generator_port import RAGGeneratorPort

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')


class CohereRAGGenerator(RAGGeneratorPort):
    """Cohere implementation for RAG response generation."""
    
    def __init__(self, model_name: str = "command-r-plus"):
        self.client = cohere.Client(COHERE_API_KEY)
        self.model_name = model_name
        
        self.rag_system_prompt = """
        You are a helpful AI assistant. Answer the user's question based on the provided context documents.
        
        Guidelines:
        - Use only information from the provided context
        - If the context doesn't contain enough information, say so clearly
        - Be concise but comprehensive
        - Cite sources when possible by mentioning the document name
        - If multiple documents contain relevant information, synthesize them coherently
        
        Context documents:
        {context}
        
        Question: {question}
        
        Answer:"""
    
    def generate_response_with_context(
        self,
        query: str,
        context_chunks: List[DocumentChunk],
        chat_history: History
    ) -> str:
        """Generate a response using the provided context chunks and chat history."""
        if not context_chunks:
            return self.generate_response_without_context(query, chat_history)
        
        # Prepare context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            source_info = f"Document {i}"
            if hasattr(chunk, 'source_document') and chunk.source_document:
                source_info += f" (from {chunk.source_document})"
            context_parts.append(f"{source_info}:\n{chunk.content}")
        
        context = "\n\n".join(context_parts)
        
        # Format the prompt
        formatted_prompt = self.rag_system_prompt.format(
            context=context,
            question=query
        )
        
        try:
            response = self.client.chat(
                model=self.model_name,
                message=formatted_prompt,
                chat_history=chat_history.chat_history,
                temperature=0.7
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"RAG generation failed: {e}")
            return self.generate_response_without_context(query, chat_history)
    
    def generate_response_without_context(
        self,
        query: str,
        chat_history: History
    ) -> str:
        """Generate a response without RAG context (fallback)."""
        try:
            response = self.client.chat(
                model=self.model_name,
                message=query,
                chat_history=chat_history.chat_history,
                temperature=0.7
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"Fallback generation failed: {e}")
            return "I encountered an error while generating a response. Please try again." 