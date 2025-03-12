import sys
import os
from dotenv import load_dotenv
import cohere

sys.stdin = open(os.devnull)

load_dotenv()
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')

class CohereTextGenerator():
    def __init__(self):
        self.client = cohere.ClientV2(COHERE_API_KEY)

    def generate_text(self, prompt: str, chat_history=None) -> str:
        if chat_history is None:
            chat_history = []
        response = self.client.chat(
            model="command-r-plus-08-2024",
            chat_history=chat_history,
            messages=[
                {"role": "system", "content": "You are an assistant, helping the user named Barat, and you answer him using rap lyrics."},
                {"role": "user", "content": prompt}]
        )
        return response.message.content[0].text