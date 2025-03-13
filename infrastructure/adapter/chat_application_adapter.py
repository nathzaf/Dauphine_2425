from domain.model.history import History
from domain.port.chat_application_port import ChatApplicationPort
from infrastructure.history_repository.history_repository import HistoryRepository
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator


class ChatApplicationAdapter(ChatApplicationPort):

    def __init__(self,
                 text_generator: CohereTextGenerator = None,
                 history_repository: HistoryRepository = None):
        self.text_generator = text_generator
        self.history_repository = history_repository

    def get_generated_text(self, prompt: str, chat_history: History) -> str:
        return self.text_generator.generate_text(prompt=prompt, chat_history=chat_history.chat_history)

    def save_history(self, history: History):
        self.history_repository.save_history(history)

    def get_history(self, chat_id: str) -> History:
        return self.history_repository.get_history(chat_id)

    def get_all_histories(self) -> list[History]:
        return self.history_repository.get_all_histories()
