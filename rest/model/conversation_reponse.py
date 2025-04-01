from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

from domain.model.role_message import RoleMessage

class ConversationResponse(BaseModel):
    guid: str = Field(default=None,
                    title="Conversation GUID", 
                    description="The ID of the conversation")
    history: list[RoleMessage] = Field(default=None,
                                title="History", 
                                description="The whole history for the conversation")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)