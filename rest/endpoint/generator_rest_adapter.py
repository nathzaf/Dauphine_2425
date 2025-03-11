from fastapi import APIRouter, HTTPException

from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse

from domain.port.generator_controller_port import GeneratorControllerPort

class GeneratorRestAdapter:
    def __init__(self, controller: GeneratorControllerPort):
        self.controller = controller

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            response = self.controller.generate_message(request.prompt)
            return ChatResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/chat")(self.chat)
        return router
