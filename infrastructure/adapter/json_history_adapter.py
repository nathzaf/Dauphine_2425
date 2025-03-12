import json
from typing import List, Dict
from domain.port.history_port import HistoryPort

class JSONHistoryAdapter(HistoryPort):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_history(self) -> Dict[str, List[Dict[str, str]]]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_history(self, history_data: Dict[str, List[Dict[str, str]]]):
        with open(self.file_path, 'w') as file:
            json.dump(history_data, file, indent=4)

    def save_message(self, conversation_id: str, role: str, message: str):
        history_data = self._load_history()
        if conversation_id not in history_data:
            history_data[conversation_id] = []
        history_data[conversation_id].append({"role": role, "content": message})
        self._save_history(history_data)

    def get_history(self, conversation_id: str) -> List[Dict[str, str]]:
        history_data = self._load_history()
        return history_data.get(conversation_id, [])

    def clear_history(self, conversation_id: str):
        history_data = self._load_history()
        if conversation_id in history_data:
            del history_data[conversation_id]
            self._save_history(history_data)