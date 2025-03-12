from domain.port.history_port import HistoryPort
from typing import List, Dict

class HistoryService:
    def __init__(self, history_port: HistoryPort):
        self.history_port = history_port

    def save_message(self, conversation_id: str, role: str, message: str):
        self.history_port.save_message(conversation_id, role, message)

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        return self.history_port.get_history(conversation_id)

    def clear_history(self, conversation_id: str):
        self.history_port.clear_history(conversation_id)