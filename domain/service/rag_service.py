from typing import List, Optional, Dict, Any
from domain.model.document import DocumentChunk
from domain.service.document_service import DocumentService
from domain.port.text_generator_port import TextGeneratorPort

class RAGService:
    def __init__(self, document_service: DocumentService, text_generator: TextGeneratorPort):
        self.document_service = document_service
        self.text_generator = text_generator

    def generate_contextual_response(self, prompt: str, chat_history: List[Dict[str, str]], 
                                   user_id: Optional[str] = None, 
                                   user_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate response using RAG approach"""
        
        # 1. Retrieve relevant documents
        relevant_chunks = self.document_service.search_relevant_content(prompt, limit=5)
        
        # 2. Build context from retrieved documents
        context_text = self._build_context_from_chunks(relevant_chunks, user_context)
        
        # 3. Generate response with context
        if context_text:
            response = self.text_generator.generate_text_with_context(
                prompt=prompt,
                chat_history=chat_history,
                context=context_text,
                user_id=user_id
            )
            
            # Add source information
            if relevant_chunks:
                sources_info = self._format_sources(relevant_chunks)
                return f"{response}\n\n📚 **Sources consultées:** {sources_info}"
            
            return response
        else:
            return self.text_generator.generate_text(prompt, chat_history)

    def _build_context_from_chunks(self, chunks: List[DocumentChunk], 
                                 user_context: Optional[Dict[str, Any]] = None) -> str:
        """Build context text from relevant document chunks"""
        if not chunks:
            return ""
        
        context_parts = []
        context_parts.append("=== INFORMATIONS PERSONNALISÉES DISPONIBLES ===")
        
        # Add user context if available
        if user_context:
            context_parts.append(f"\nInformations utilisateur:")
            context_parts.append(f"- Nom: {user_context.get('first_name', '')} {user_context.get('last_name', '')}")
            context_parts.append(f"- N° allocataire: {user_context.get('id_number', '')}")
            context_parts.append(f"- Date de naissance: {user_context.get('birth_date', '')}")
        
        for i, chunk in enumerate(chunks, 1):
            title = chunk.metadata.get("original_title", "Document")
            doc_type = chunk.metadata.get("document_type", "")
            
            context_parts.append(f"\n[Document {i}: {title} - {doc_type}]")
            context_parts.append(chunk.content)
        
        context_parts.append("\n=== FIN DES INFORMATIONS ===")
        return "\n".join(context_parts)

    def _format_sources(self, chunks: List[DocumentChunk]) -> str:
        """Format source information for display"""
        sources = set()
        for chunk in chunks:
            title = chunk.metadata.get("original_title", "Document")
            doc_type = chunk.metadata.get("document_type", "")
            sources.add(f"{title} ({doc_type})")
        
        return ", ".join(sources) 