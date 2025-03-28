from domain.model.chat_history import ChatHistory
from domain.port.generator_controller_port import GeneratorControllerPort

from domain.service.chat_history_service import ChatHistoryService
from domain.service.text_generation_service import TextGenerationService

# Adaptateur pour le contrôleur, implémente l'interface définie par GeneratorControllerPort
class GeneratorControllerAdapter(GeneratorControllerPort):
    def __init__(self,
                text_generation_service: TextGenerationService = None,
                chat_history_service: ChatHistoryService = None):
        self.text_generation_service = text_generation_service
        self.chat_history_service = chat_history_service
        
    def generate_message(self, prompt: str) -> str:
        generated_text = self.text_generation_service.get_generated_text(prompt)
        self.chat_history_service.add_message(prompt, generated_text, "assistant")
        return generated_text
    
    def get_conversations(self) -> list[str]:
        return self.chat_history_service.get_all_conversations()
    
    def get_history(self, conversation_guid: str) -> ChatHistory:
        return self.chat_history_service.get_history(conversation_guid)
    
    def clear_history(self, conversation_guid: str) -> ChatHistory:
        return self.chat_history_service.clear_history(conversation_guid)