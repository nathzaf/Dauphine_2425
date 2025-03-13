from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from rest.model.role_message_request import RoleMessageRequest


class HistoryItem(BaseModel):
    chat_id: str = Field(title="Chat ID", description="L'identifiant unique de la conversation")
    chat_history: list[RoleMessageRequest] = Field(title="Historique", description="L'historique de la conversation")


class AllHistoriesResponse(BaseModel):
    histories: list[HistoryItem] = Field(title="Historiques",
                                         description="Liste de tous les historiques de conversation")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)