from domain.port.generator_controller_port import GeneratorControllerPort
from domain.service.text_generation_service import TextGenerationService
from domain.service.history_service import HistoryService

class GeneratorControllerAdapter(GeneratorControllerPort):
    
    def __init__(self,
                text_generation_service: TextGenerationService,
                history_service: HistoryService):
        self.text_generation_service = text_generation_service
        self.history_service = history_service
        
    def generate_message(self, conversation_id: str, prompt: str) -> str:
        self.history_service.save_message(conversation_id, "user", prompt)
        response = self.text_generation_service.get_generated_text(prompt)
        self.history_service.save_message(conversation_id, "assistant", response)
        return response