import os
from dataclasses import dataclass
from dotenv import load_dotenv
import cohere

from domain.port.text_generator_port import TextGeneratorPort

from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

@dataclass
class TextGeneratorAdapter(TextGeneratorPort):
    cohere_text_generator: CohereTextGenerator = CohereTextGenerator()

    def get_generated_text(self, prompt: str) -> str:
        return self.cohere_text_generator.generate_text(prompt=prompt)