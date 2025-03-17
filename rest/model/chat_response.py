from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

# Modèle pour structurer et valider les réponses de l'API
class ChatResponse(BaseModel):
    # Champ pour la réponse générée
    response: str = Field(title="Response", 
                          description="The generated response")

    # Convertit l'instance en dictionnaire JSON-compatible
    def to_dict(self) -> dict:
        return jsonable_encoder(self)