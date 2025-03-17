from domain.port.generator_controller_port import GeneratorControllerPort

from domain.service.text_generation_service import TextGenerationService

# Adaptateur pour le contrôleur, implémente l'interface définie par GeneratorControllerPort
class GeneratorControllerAdapter(GeneratorControllerPort):
    
    def __init__(self,
                text_generation_service: TextGenerationService = None):
        # Injection du service de génération de texte
        self.text_generation_service = text_generation_service
        
    def generate_message(self, prompt: str) -> str:
        # Appelle le service pour générer un texte à partir du prompt
        return self.text_generation_service.get_generated_text(prompt)