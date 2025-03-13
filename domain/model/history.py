from domain.model.role_message import RoleMessage

class History:

    def __init__(self, chat_id: str, chat_history: list[RoleMessage]):
        self.chat_id = chat_id
        self.chat_history = chat_history

    def add(self, item: RoleMessage):
        self.chat_history.append(item)

    def __getter__(self):
        return self.chat_history