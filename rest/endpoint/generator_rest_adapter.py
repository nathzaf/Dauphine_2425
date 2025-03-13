from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.port.generator_controller_port import GeneratorControllerPort
from rest.model.all_histories_response import AllHistoriesResponse, HistoryItem
from rest.model.chat_request import ChatRequest
from rest.model.chat_response import ChatResponse
from rest.model.history_request import HistoryRequest
from rest.model.history_response import HistoryResponse
from rest.model.role_message_request import RoleMessageRequest


class GeneratorRestAdapter:
    def __init__(self, controller: GeneratorControllerPort):
        self.controller = controller

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            response = self.controller.generate_message(request.prompt, chat_history=request.chat_history)
            return ChatResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def save_history(self, request: HistoryRequest) -> HTTPStatus:
        try:
            messages_list = []
            for item in request.chat_history:
                messages_list.append(RoleMessage(role=item.role, message=item.message))

            history = History(chat_id=request.chat_id, chat_history=messages_list)

            self.controller.save_history(history)

            return HTTPStatus.CREATED
        except Exception as e:
            print(e.with_traceback())
            raise HTTPException(status_code=500, detail=str(e))

    async def get_history(self, chat_id: str) -> HistoryResponse:
        try:
            history = self.controller.get_history(chat_id)

            messages = [
                RoleMessageRequest(role=msg.role, message=msg.message)
                for msg in history.chat_history
            ]
            return HistoryResponse(chat_history=messages)
        except Exception as e:
            print(e.with_traceback())
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_histories(self) -> AllHistoriesResponse:
        try:
            histories = self.controller.get_all_histories()

            history_items = []
            for history in histories:
                messages = [
                    RoleMessageRequest(role=msg.role, message=msg.message)
                    for msg in history.chat_history
                ]
                history_items.append(HistoryItem(chat_id=history.chat_id, chat_history=messages))

            return AllHistoriesResponse(histories=history_items)
        except Exception as e:
            print(e.with_traceback())
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        router = APIRouter()
        router.post("/chat")(self.chat)
        router.get("/histories/{chat_id}")(self.get_history)
        router.post("/histories")(self.save_history)
        router.get("/histories")(self.get_all_histories)
        return router
