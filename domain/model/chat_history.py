from dataclasses import dataclass
from typing import List
from domain.model.role_message import RoleMessage

@dataclass
class ChatHistory:
    messages: list[RoleMessage]
