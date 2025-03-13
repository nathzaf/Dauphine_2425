from domain.model.history import History
from domain.port.chat_application_port import ChatApplicationPort


class TextGenerationService:
    def __init__(self, chat_application_port: ChatApplicationPort = None):
        self.chat_application_port = chat_application_port

    def get_generated_text(self, prompt: str, chat_history: History) -> str:
        return self.chat_application_port.get_generated_text(prompt, chat_history)
