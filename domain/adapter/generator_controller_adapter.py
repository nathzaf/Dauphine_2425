from domain.model.history import History
from domain.model.role_message import RoleMessage
from domain.port.generator_controller_port import GeneratorControllerPort
from domain.service.history_service import HistoryService

from domain.service.text_generation_service import TextGenerationService
from rest.model.role_message_request import RoleMessageRequest


class GeneratorControllerAdapter(GeneratorControllerPort):

    def __init__(self,
                 text_generation_service: TextGenerationService = None,
                 history_service: HistoryService = None):
        self.history_service = history_service
        self.text_generation_service = text_generation_service

    def generate_message(self, prompt: str, chat_history: list[RoleMessageRequest]) -> str:
        role_messages = [RoleMessage(role=message.role, message=message.message) for message in chat_history]
        return self.text_generation_service.get_generated_text(prompt, History(chat_id="", chat_history=role_messages))

    def save_history(self, history: History):
        self.history_service.save_history(history)

    def get_history(self, chat_id: str) -> History:
        return self.history_service.get_history(chat_id)

    def get_all_histories(self) -> list[History]:
        return self.history_service.get_all_histories()
