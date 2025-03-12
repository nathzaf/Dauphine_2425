import json
from typing import List, Dict
from domain.port.history_port import HistoryPort

class JSONHistoryAdapter(HistoryPort):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._load_history()

    def _load_history(self):
        try:
            with open(self.file_path, 'r') as file:
                self.history_data = json.load(file)
        except FileNotFoundError:
            self.history_data = {}

    def _save_history(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.history_data, file, indent=4)

    def save_message(self, conversation_id: str, role: str, message: str):
        if conversation_id not in self.history_data:
            self.history_data[conversation_id] = []
        self.history_data[conversation_id].append({"role": role, "content": message})
        self._save_history()

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        return self.history_data.get(conversation_id, [])

    def clear_history(self, conversation_id: str):
        if conversation_id in self.history_data:
            del self.history_data[conversation_id]
            self._save_history()