import os
from dotenv import load_dotenv
import cohere

# Import du port pour définir l'interface à implémenter
from domain.port.text_generator_port import TextGeneratorPort

# Import du générateur de texte Cohere
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere

class TextGeneratorAdapter(TextGeneratorPort):
    def __init__(self, cohere_text_generator: CohereTextGenerator):
        """
        Adaptateur pour connecter le port TextGeneratorPort à l'implémentation CohereTextGenerator.
        :param cohere_text_generator: Instance de CohereTextGenerator.
        """
        self.cohere_text_generator = cohere_text_generator

    def get_generated_text(self, prompt: str) -> str:
        """
        Implémente la méthode du port pour générer du texte.
        :param prompt: Le message utilisateur.
        :return: La réponse générée par Cohere.
        """
        return self.cohere_text_generator.generate_text(prompt=prompt)