
import os
from dotenv import load_dotenv
import cohere

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

class CohereTextGenerator():
    def __init__(self):
        self.client = cohere.Client(COHERE_API_KEY)

    def generate_text(self, prompt: str) -> str:
        response = self.client.chat(
            # chat_history=chat_history,
            message=prompt
        )
        return response.text