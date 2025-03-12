from pydantic import BaseModel

class HistoryRequest(BaseModel):
    conversation_id: str
    role: str
    message: str