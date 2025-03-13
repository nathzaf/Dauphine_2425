import json
import os

from domain.model.history import History
from domain.model.role_message import RoleMessage


class HistoryRepository:

    def __init__(self):
        self.path = './data/history.json'

    def get_history(self, chat_id: str) -> History:

        with open(self.path, 'r') as file:
            data = json.load(file)

        for entry in data:
            if entry.get("chat_id") == chat_id:
                history = []
                for item in entry.get("chat_history", []):
                    history.append(RoleMessage(item["role"], item["message"]))

                return History(chat_id, history)

        return History(chat_id, [])

    def get_all_histories(self) -> list[History]:
        histories = []

        with open(self.path, 'r') as file:
            data = json.load(file)

        for entry in data:
            chat_id = entry.get("chat_id")
            history = []
            for item in entry.get("chat_history", []):
                # Gestion du cas où item est une liste au lieu d'un dictionnaire
                if isinstance(item, list):
                    for inner_item in item:
                        if isinstance(inner_item, dict) and "role" in inner_item and "message" in inner_item:
                            history.append(RoleMessage(inner_item["role"], inner_item["message"]))
                # Cas normal où item est un dictionnaire
                elif isinstance(item, dict) and "role" in item and "message" in item:
                    history.append(RoleMessage(item["role"], item["message"]))

            histories.append(History(chat_id, history))

        return histories

    def save_history(self, history: History):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as file:
                json.dump([], file)

        with open(self.path, 'r+') as file:
            data = json.load(file)

            for entry in data:
                if entry.get("chat_id") == history.chat_id:
                    for msg in history.chat_history:
                        entry["chat_history"].append(msg.__dict__)
                    break
            else:
                data.append({
                    "chat_id": history.chat_id,
                    "chat_history": [msg.__dict__ for msg in history.chat_history]
                })

            file.seek(0)
            json.dump(data, file)
            file.truncate()
