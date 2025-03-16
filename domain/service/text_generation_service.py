from domain.port.text_generator_port import TextGeneratorPort

class TextGenerationService:
    def __init__(self, text_generator: TextGeneratorPort):
        self.text_generator = text_generator

    def get_generated_text(self, prompt: str) -> str:
        return self.text_generator.get_generated_text(prompt)