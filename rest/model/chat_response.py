from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

class ChatResponse(BaseModel):
    response: str = Field(title="Response", 
                        description="The generated response")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)