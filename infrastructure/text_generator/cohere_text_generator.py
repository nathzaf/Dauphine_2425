import os
from dotenv import load_dotenv
import cohere

from domain.service.system_prompt_service import SystemPromptService

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere depuis les variables d'environnement

#systemPrompt = "Answer the user named Guillaume question by rapping"

class CohereTextGenerator():
    def __init__(self,system_prompt_service: SystemPromptService ):
        # Initialise le client Cohere avec la clé API
        self.client = cohere.ClientV2(COHERE_API_KEY)
        self.system_prompt_service = system_prompt_service

    def generate_text(self, prompt: str) -> str:
        # Récupérer le system prompt depuis le service
        system_prompt = self.system_prompt_service.get_system_prompt()

        response = self.client.chat(
            # chat_history=chat_history,  
            model="command-r",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "assistant", "content": "Hello! How can I help you?"},
                      {"role": "user", "content": prompt}]
        )
        return response.message.content[0].text  # Retourne le texte généré par Cohere