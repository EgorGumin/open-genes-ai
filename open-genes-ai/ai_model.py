from abc import ABC, abstractmethod


class AIModel(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Process the input prompt and return the model's response.

        Args:
            prompt: Input text prompt for the model.

        Returns:
            Model's response as a string.
        """
        pass
