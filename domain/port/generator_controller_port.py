from abc import ABC, abstractmethod

class GeneratorControllerPort(ABC):
    @abstractmethod
    def generate_message(self, prompt: str) -> str:
        pass