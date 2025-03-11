from domain.adapter.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.text_generation_service import TextGenerationService

from infrastructure.adapter.text_generator_adapter import TextGeneratorAdapter

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter

def create_generator_rest_adapter():
    text_generator_adapter = TextGeneratorAdapter()
    text_generation_service = TextGenerationService(text_generator_adapter)
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service)
    return GeneratorRestAdapter(generator_controller_adapter)
