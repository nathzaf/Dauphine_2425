from domain.model.system_prompt import SystemPrompt

class SystemPromptService:
    def __init__(self):
        # Initialisez le prompt par défaut
        self.system_prompt = SystemPrompt(
            content="You are an assistant, helping a user answering his questions"
        )

    def get_system_prompt(self) -> str:
        return self.system_prompt.content

    def set_system_prompt(self, content: str):
        self.system_prompt.content = content