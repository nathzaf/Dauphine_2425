import os
from dotenv import load_dotenv
import cohere

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere depuis les variables d'environnement



class CohereTextGenerator():
    def __init__(self):
        # Initialise le client Cohere avec la clé API
        self.client = cohere.Client(COHERE_API_KEY)

    def generate_text(self, prompt: str) -> str:
        """
        Génère une réponse textuelle à partir d'un prompt en utilisant l'API Cohere.
        :param prompt: Le message utilisateur pour lequel une réponse est générée.
        :return: La réponse générée par Cohere.
        """
        response = self.client.chat(
            # chat_history=chat_history,  
            message=prompt  # Le message utilisateur
        )
        return response.text  # Retourne le texte généré par Cohere