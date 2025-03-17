from domain.adapter.generator_controller_adapter import GeneratorControllerAdapter
from domain.service.text_generation_service import TextGenerationService
from domain.service.system_prompt_service import SystemPromptService  # Nouveau service

from infrastructure.adapter.text_generator_adapter import TextGeneratorAdapter
from infrastructure.text_generator.cohere_text_generator import CohereTextGenerator  # Import du générateur Cohere

from rest.endpoint.generator_rest_adapter import GeneratorRestAdapter

def create_generator_rest_adapter():
    # Initialiser le service pour le system prompt
    system_prompt_service = SystemPromptService()

    # Initialiser le générateur Cohere avec le service de prompt
    cohere_text_generator = CohereTextGenerator(system_prompt_service)

    # Injecter CohereTextGenerator dans TextGeneratorAdapter
    text_generator_adapter = TextGeneratorAdapter(cohere_text_generator=cohere_text_generator)

    # Configurer les services et adaptateurs
    text_generation_service = TextGenerationService(text_generator_adapter)
    generator_controller_adapter = GeneratorControllerAdapter(text_generation_service)
    return GeneratorRestAdapter(generator_controller_adapter)
