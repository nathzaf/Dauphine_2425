from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class RoleMessageRequest(BaseModel):
    role: str
    message: str

    def to_dict(self) -> dict:
        return jsonable_encoder(self)
