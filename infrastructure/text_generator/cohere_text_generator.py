import os
from dotenv import load_dotenv
import cohere

from domain.model.chat_history import ChatHistory

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere depuis les variables d'environnement

def to_chat_messages(chat_history: ChatHistory) -> list[dict]:
    """Convertit l'historique de chat en une liste de dictionnaires avec le format attendu par Cohere."""   
    return [{"role": msg.role, "content": msg.message} for msg in chat_history.messages]

class CohereTextGenerator():
    def __init__(self):
        # Initialise le client Cohere avec la clé API
        self.client = cohere.ClientV2(COHERE_API_KEY)

    def generate_text(self, chat_history: ChatHistory) -> str:
        # system_prompt = self.system_prompt_service.get_system_prompt()
        
        response = self.client.chat(
            model="command-r",
            messages=to_chat_messages(chat_history)
        )
        return response.message.content[0].text # Retourne le texte généré par Cohere