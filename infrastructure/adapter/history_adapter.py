import json
from typing import List, Dict
from domain.port.history_port import HistoryPort

class HistoryAdapter(HistoryPort):
    def __init__(self):
        self.history_data = {}

    def save_message(self, conversation_id: str, role: str, message: str):
        if conversation_id not in self.history_data:
            self.history_data[conversation_id] = []
        self.history_data[conversation_id].append({"role": role, "content": message})

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        return self.history_data.get(conversation_id, [])

    def clear_history(self, conversation_id: str):
        if conversation_id in self.history_data:
            del self.history_data[conversation_id]