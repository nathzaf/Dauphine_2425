from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

class ChatRequest(BaseModel):
    prompt: str = Field(title="Prompt", 
                        description="The message to generate a response for", 
                        default="Hello world!")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)