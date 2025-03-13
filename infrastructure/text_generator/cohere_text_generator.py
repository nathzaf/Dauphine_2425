import os

import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')


class CohereTextGenerator:
    def __init__(self):
        self.client = cohere.Client(COHERE_API_KEY)

    def generate_text(self, prompt: str, chat_history: list) -> str:
        response = self.client.chat(
            chat_history=chat_history,
            message=prompt
        )
        return response.text
