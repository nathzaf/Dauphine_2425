import os
import json
import uuid
from typing import Optional
from dataclasses import asdict

from domain.model.chat_history import ChatHistory
from domain.model.role_message import RoleMessage

class JsonHistoryRepository:
    def __init__(self, storage_folder: str):
        """
        Initialize the repository with a folder to store JSON files.
        """
        self.storage_folder = storage_folder
        os.makedirs(self.storage_folder, exist_ok=True)
        
    def get_all_conversations(self) -> list[str]:
        """
        Retrieve all conversation GUIDs stored in the JSON files.
        Returns a list of GUIDs.
        """
        files = os.listdir(self.storage_folder)
        return [file.split('.')[0] for file in files if file.endswith('.json')]

    def create_conversation(self) -> str:
        """
        Create and save a conversation as a JSON file named with a GUID.
        Returns the GUID of the created conversation.
        """
        new_conversation_id = str(uuid.uuid4())
        file_path = os.path.join(self.storage_folder, f"{new_conversation_id}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(ChatHistory(messages={})), file, ensure_ascii=False, indent=4)
        return new_conversation_id

    def add_entry_to_conversation(self, conversation_id: str, new_entry: RoleMessage) -> Optional[ChatHistory]:
        """
        Add a new entry (RoleMessage) into the associated JSON file.
        """
        chat_history = self.get_history_from_file(conversation_id)
        if chat_history is None:
            return None
        chat_history.messages.append(new_entry)
        file_path = os.path.join(self.storage_folder, f"{conversation_id}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(chat_history), file, ensure_ascii=False, indent=4)
        return self.get_history_from_file(conversation_id)

    def get_history_from_file(self, conversation_id: str) -> Optional[ChatHistory]:
        """
        Retrieve a ChatHistory object from a JSON file.
        Returns None if the file does not exist.
        """
        file_path = os.path.join(self.storage_folder, f"{conversation_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = [RoleMessage(**msg) for msg in data.get('messages', [])]
            return ChatHistory(messages)

    def clear_conversation(self, conversation_id: str) -> Optional[ChatHistory]:
        """
        Clear a conversation by emptying the file.
        Returns True if successful, False if the file does not exist.
        """
        file_path = os.path.join(self.storage_folder, f"{conversation_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(ChatHistory(messages={})), file, ensure_ascii=False, indent=4)
        return self.get_history_from_file(conversation_id)