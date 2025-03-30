from abc import ABC, abstractmethod

class TextGeneratorPort(ABC):
    @abstractmethod
    def get_generated_text(self, prompt: str) -> str:
        pass