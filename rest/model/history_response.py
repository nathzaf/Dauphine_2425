from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from rest.model.role_message_request import RoleMessageRequest


class HistoryResponse(BaseModel):
    chat_history: list[RoleMessageRequest] = Field(title="History",
                                                   description="The chat history")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)
