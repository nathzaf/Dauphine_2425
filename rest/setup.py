from domain.adapter.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.history_service import HistoryService
from domain.service.text_generation_service import TextGenerationService
from infrastructure.adapter.chat_application_adapter import ChatApplicationAdapter
from infrastructure.history_repository.history_repository import HistoryRepository
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter


def create_generator_rest_adapter():
    text_generator = CohereTextGenerator()
    history_repository = HistoryRepository()
    chat_application_adapter = ChatApplicationAdapter(text_generator=text_generator,
                                                      history_repository=history_repository)
    history_service = HistoryService(chat_application_adapter)
    text_generation_service = TextGenerationService(chat_application_adapter)
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service, history_service)
    return GeneratorRestAdapter(generator_controller_adapter)
