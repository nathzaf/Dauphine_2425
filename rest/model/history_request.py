from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from rest.model.role_message_request import RoleMessageRequest


class HistoryRequest(BaseModel):
    chat_id: str = Field(title="Chat ID",
                         description="The chat ID")
    chat_history: list[RoleMessageRequest] = Field(title="Chat History",
                                                   description="The chat history")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)
