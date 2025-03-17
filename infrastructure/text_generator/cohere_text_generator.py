import os
from dotenv import load_dotenv
import cohere

from domain.service.system_prompt_service import SystemPromptService
from domain.service.chat_history_service import ChatHistoryService

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere depuis les variables d'environnement

class CohereTextGenerator():
    def __init__(self,system_prompt_service: SystemPromptService, chat_history_service: ChatHistoryService ):
        # Initialise le client Cohere avec la clé API
        self.client = cohere.ClientV2(COHERE_API_KEY)
        self.system_prompt_service = system_prompt_service
        self.chat_history_service = chat_history_service

    def generate_text(self, prompt: str) -> str:
        # Récupérer le system prompt depuis le service
        system_prompt = self.system_prompt_service.get_system_prompt()

        # Construire l'historique des messages
        chat_history = [
            {"role": msg.role, "content": msg.message}
            for msg in self.chat_history_service.get_history()
        ]

        response = self.client.chat(
            # chat_history=chat_history,  
            model="command-r",
            messages=[{"role": "system", "content": system_prompt}]+
                      chat_history+
                      [{"role": "user", "content": prompt}]
        )

        # Ajouter la réponse de l'assistant à l'historique
        bot_response = response.message.content[0].text
        self.chat_history_service.add_message("user", prompt)
        self.chat_history_service.add_message("assistant", bot_response)

        return response.message.content[0].text  # Retourne le texte généré par Cohere