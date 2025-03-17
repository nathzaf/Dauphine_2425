from typing import List
from domain.model.role_message import RoleMessage

class ChatHistory:
    def __init__(self):
        self.messages: List[RoleMessage] = []
