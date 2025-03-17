from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

# Modèle pour valider les requêtes de chat
class ChatRequest(BaseModel):
    # chat_history: list
    # prompt : message utilisateur pour générer une réponse
    prompt: str = Field(title="Prompt", 
                        description="The message to generate a response for", 
                        default="Hello world!")

    # Convertit l'instance en dictionnaire JSON-compatible
    def to_dict(self) -> dict:
        return jsonable_encoder(self)