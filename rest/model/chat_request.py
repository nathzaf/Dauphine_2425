from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from rest.model.role_message_request import RoleMessageRequest


class ChatRequest(BaseModel):
    chat_history: list[RoleMessageRequest]
    prompt: str = Field(title="Prompt",
                        description="The message to generate a response for",
                        default="Hello world!")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)
