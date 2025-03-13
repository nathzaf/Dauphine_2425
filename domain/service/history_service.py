from domain.model.history import History
from domain.port.chat_application_port import ChatApplicationPort


class HistoryService:
    def __init__(self, chat_application_port: ChatApplicationPort = None):
        self.chat_application_port = chat_application_port

    def save_history(self, history: History):
        self.chat_application_port.save_history(history)

    def get_history(self, chat_id: str) -> History:
        return self.chat_application_port.get_history(chat_id)

    def get_all_histories(self) -> list[History]:
        return self.chat_application_port.get_all_histories()
