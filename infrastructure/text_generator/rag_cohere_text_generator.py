import os
from typing import List, Optional, Dict, Any
import cohere
from dotenv import load_dotenv

from domain.model.document import DocumentChunk
from domain.service.document_service import DocumentService

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

class RAGCohereTextGenerator:
    def __init__(self, document_service: DocumentService = None):
        self.client = cohere.Client(COHERE_API_KEY)
        self.document_service = document_service

    def generate_text_with_context(self, prompt: str, chat_history: list, 
                                   user_id: Optional[str] = None, 
                                   user_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate text using RAG - retrieve relevant documents first"""
        
        # 1. Retrieve relevant documents based on the prompt
        relevant_chunks = []
        if self.document_service and user_id:
            relevant_chunks = self.document_service.search_relevant_documents(prompt, limit=5)
            print(f"Found {len(relevant_chunks)} relevant chunks for user {user_id}")
        
        # 2. Build context from retrieved documents
        context_text = self._build_context_from_chunks(relevant_chunks, user_id, user_context)
        
        # 3. Enhance the prompt with context
        enhanced_prompt = self._enhance_prompt_with_context(prompt, context_text, user_context)
        
        # 4. Generate response using Cohere
        try:
            response = self.client.chat(
                chat_history=chat_history,
                message=enhanced_prompt
            )
            
            # 5. Add sources information if relevant documents were found
            if relevant_chunks:
                sources_info = self._format_sources(relevant_chunks)
                return f"{response.text}\n\n📚 **Sources consultées:** {sources_info}"
            
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return "Désolé, je rencontre des difficultés techniques pour accéder à vos documents. Pouvez-vous reformuler votre question ?"

    def _build_context_from_chunks(self, chunks: List[DocumentChunk], 
                                   user_id: Optional[str] = None, 
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

    def _enhance_prompt_with_context(self, original_prompt: str, context: str, 
                                     user_context: Optional[Dict[str, Any]] = None) -> str:
        """Enhance the user prompt with retrieved context"""
        user_name = ""
        if user_context:
            user_name = f"{user_context.get('first_name', '')} {user_context.get('last_name', '')}"
        
        if not context:
            base_prompt = f"""Vous êtes un assistant de la CAF (Caisse d'Allocations Familiales). 
Répondez en français de manière professionnelle et utile."""
            if user_name:
                base_prompt += f" Vous vous adressez à {user_name}."
            return f"{base_prompt}\n\nQUESTION: {original_prompt}"
        
        enhanced_prompt = f"""Vous êtes un assistant personnalisé de la CAF (Caisse d'Allocations Familiales). 
Vous avez accès aux documents personnalisés de l'utilisateur.

{context}

QUESTION DE L'UTILISATEUR: {original_prompt}

INSTRUCTIONS:
- Répondez en français de manière professionnelle
- Utilisez UNIQUEMENT les informations fournies ci-dessus pour répondre
- Si les informations ne permettent pas de répondre complètement, indiquez-le clairement
- Soyez précis et personnalisé dans votre réponse
- Référez-vous aux documents spécifiques quand nécessaire"""

        if user_name:
            enhanced_prompt += f"\n- Vous vous adressez à {user_name}"

        return enhanced_prompt

    def _format_sources(self, chunks: List[DocumentChunk]) -> str:
        """Format source information for display"""
        sources = set()
        for chunk in chunks:
            title = chunk.metadata.get("original_title", "Document")
            doc_type = chunk.metadata.get("document_type", "")
            sources.add(f"{title} ({doc_type})")
        
        return ", ".join(sources)

    def generate_text(self, prompt: str, chat_history: list) -> str:
        """Fallback method for compatibility"""
        return self.generate_text_with_context(prompt, chat_history) 