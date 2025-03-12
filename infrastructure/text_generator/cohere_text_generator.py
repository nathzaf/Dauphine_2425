
import os
from dotenv import load_dotenv
import cohere

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

class CohereTextGenerator():
    def __init__(self):
        self.client = cohere.ClientV2(COHERE_API_KEY)

    def generate_text(self, prompt: str) -> str:
        response = self.client.chat(
            model="command-r-plus-08-2024",
            # chat_history=chat_history,
            messages=[
                {"role": "system", "content": "You are an assistant, helping the user named Barat, and you answer him using rap lyrics."},
                {"role": "user", "content": prompt}]
        )
        return response.message.content[0].text