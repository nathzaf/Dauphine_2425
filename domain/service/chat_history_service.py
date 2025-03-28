from domain.model.chat_history import ChatHistory
from domain.model.role_message import RoleMessage
from domain.port.chat_history_port import ChatHistoryPeristencePort

class ChatHistoryService:
    def __init__(self, history_handler: ChatHistoryPeristencePort):
        self.history_handler = history_handler
        
    def get_all_conversations(self) -> list[str]:
        return self.history_handler.get_all_conversations()

    def get_history(self) -> ChatHistory:
        return self.history_handler.get_history()

    def add_message(self, conversation_guid: str, role_message: RoleMessage) -> ChatHistory:
        return self.history_handler.add_message_to_history(conversation_guid, role_message)

    def clear_history(self, conversation_guid: str) -> ChatHistory:
        return self.history_handler.clear_history(conversation_guid)