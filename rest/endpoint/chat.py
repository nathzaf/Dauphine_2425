from fastapi import APIRouter, HTTPException
from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse
from rest.model.history_request import HistoryRequest
from rest.dependencies import generator_controller_adapter as controller
from rest.dependencies import history_service

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = controller.generate_message(request.prompt)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    try:
        history = history_service.get_history(conversation_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history")
async def save_history(request: HistoryRequest):
    try:
        history_service.save_message(request.conversation_id, request.role, request.message)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))