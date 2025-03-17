import os
from dataclasses import dataclass
from dotenv import load_dotenv
import cohere

# Import du port pour définir l'interface à implémenter
from domain.port.text_generator_port import TextGeneratorPort

# Import du générateur de texte Cohere
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')  # Récupère la clé API Cohere

@dataclass
class TextGeneratorAdapter(TextGeneratorPort):
    """
    Adaptateur pour connecter le port TextGeneratorPort à l'implémentation CohereTextGenerator.
    """
    cohere_text_generator: CohereTextGenerator = CohereTextGenerator()  # Instance du générateur Cohere

    def get_generated_text(self, prompt: str) -> str:
        """
        Implémente la méthode du port pour générer du texte.
        :param prompt: Le message utilisateur.
        :return: La réponse générée par Cohere.
        """
        return self.cohere_text_generator.generate_text(prompt=prompt)