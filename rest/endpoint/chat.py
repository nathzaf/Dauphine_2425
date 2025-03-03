from fastapi import APIRouter, HTTPException

from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse
from rest.dependencies import generator_controller_adapter as controller

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = controller.generate_message(request.prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
