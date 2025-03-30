from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

from domain.model.chat_history import ChatHistory

class ConversationResponse(BaseModel):
    guid: str = Field(default=None,
                    title="Conversation GUID", 
                    description="The ID of the conversation")
    history: ChatHistory = Field(default=None,
                                title="History", 
                                description="The chat history for the conversation")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)