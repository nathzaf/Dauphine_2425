from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

class SinglePromptResponse(BaseModel):
    response: str = Field(default=None,
                        title="Response", 
                        description="The generated response")

    def to_dict(self) -> dict:
        return jsonable_encoder(self)