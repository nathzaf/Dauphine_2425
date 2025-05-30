import os
from typing import List, Dict, Optional
import cohere
from dotenv import load_dotenv

from domain.port.text_generator_port import TextGeneratorPort

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

class CohereTextGeneratorAdapter(TextGeneratorPort):
    def __init__(self):
        self.client = cohere.Client(COHERE_API_KEY)

    def generate_text(self, prompt: str, chat_history: List[Dict[str, str]]) -> str:
        """Generate text using Cohere without additional context"""
        try:
            response = self.client.chat(
                chat_history=chat_history,
                message=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return "Désolé, je rencontre des difficultés techniques. Pouvez-vous reformuler votre question ?"

    def generate_text_with_context(self, prompt: str, chat_history: List[Dict[str, str]], 
                                   context: str, user_id: Optional[str] = None) -> str:
        """Generate text using Cohere with additional context"""
        try:
            enhanced_prompt = self._enhance_prompt_with_context(prompt, context, user_id)
            
            response = self.client.chat(
                chat_history=chat_history,
                message=enhanced_prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating text with context: {e}")
            return "Désolé, je rencontre des difficultés techniques pour accéder à vos documents. Pouvez-vous reformuler votre question ?"

    def _enhance_prompt_with_context(self, original_prompt: str, context: str, user_id: Optional[str] = None) -> str:
        """Enhance the user prompt with retrieved context"""
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

        return enhanced_prompt 