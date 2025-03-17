from domain.model.chat_history import ChatHistory
from domain.model.role_message import RoleMessage

class ChatHistoryService:
    def __init__(self):
        self.chat_history = ChatHistory()

    def add_message(self, role: str, message: str):
        self.chat_history.messages.append(RoleMessage(role=role, message=message))

    def get_history(self):
        return self.chat_history.messages

    def clear_history(self):
        self.chat_history.messages = []