from fastapi import APIRouter, HTTPException

# Import des modèles pour valider les requêtes et réponses
from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse

# Import du port du contrôleur pour la logique métier
from domain.port.generator_controller_port import GeneratorControllerPort

# Adaptateur REST pour gérer les requêtes HTTP
class GeneratorRestAdapter:
    def __init__(self, controller: GeneratorControllerPort):
        """
        Initialise l'adaptateur avec un contrôleur.
        """
        self.controller = controller

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Gère les requêtes POST à /chat et génère une réponse.
        """
        try:
            # Appelle le contrôleur pour générer une réponse
            response = self.controller.generate_message(request.prompt)
            
            # Retourne la réponse encapsulée
            return ChatResponse(response=response)
        except Exception as e:
            # Lève une exception HTTP en cas d'erreur
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        """
        Configure et retourne un routeur FastAPI.
        """
        router = APIRouter()  # Crée un routeur
        router.post("/chat")(self.chat)  # Associe /chat à la méthode chat
        return router  # Retourne le routeur
