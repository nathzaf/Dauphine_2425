from domain.model.chat_history import ChatHistory
from domain.port.driven.text_generator_port import TextGeneratorPort

class TextGenerationService:
    def __init__(self, text_generator: TextGeneratorPort):
        self.text_generator = text_generator

    def get_generated_text(self, chat_history: ChatHistory) -> str:
        return self.text_generator.get_generated_text(chat_history)