
from domain.port.generator_controller_port import GeneratorControllerPort

from domain.service.text_generation_service import TextGenerationService


class GeneratorControllerAdapter(GeneratorControllerPort):
    
    def __init__(self,
                text_generation_service: TextGenerationService = None):
        self.text_generation_service = text_generation_service
        
    def generate_message(self, prompt: str) -> str:
        return self.text_generation_service.get_generated_text(prompt)