from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    sender: str
    message: str
    timestamp: str

class ChatHistory(BaseModel):
    conversation_id: str
    messages: List[ChatMessage]