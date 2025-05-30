from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from rest.model.role_message_request import RoleMessageRequest


class ChatRequest(BaseModel):
    chat_history: list[RoleMessageRequest]
    prompt: str = Field(title="Prompt",
                        description="The message to generate a response for",
                        default="Hello world!")
    user_id: Optional[str] = Field(title="User ID", 
                                   description="The user ID for document context",
                                   default=None)
    user_context: Optional[Dict[str, Any]] = Field(title="User Context",
                                                   description="Additional user context",
                                                   default=None)

    def to_dict(self) -> dict:
        return jsonable_encoder(self)
