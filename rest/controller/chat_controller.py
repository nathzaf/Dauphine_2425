from fastapi import APIRouter, HTTPException
from application.use_case.chat_use_case import ChatUseCase
from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse

class ChatController:
    def __init__(self, chat_use_case: ChatUseCase):
        self.chat_use_case = chat_use_case

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            # Convert chat history to the expected format
            chat_history = [
                {"role": msg.role, "message": msg.message} 
                for msg in request.chat_history
            ]
            
            response = self.chat_use_case.generate_chat_response(
                prompt=request.prompt,
                chat_history=chat_history,
                user_id=request.user_id,
                user_context=request.user_context
            )
            return ChatResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/chat")(self.chat)
        return router 