import os
from abc import ABC
from openai import OpenAI


class AIModel(ABC):
    def __init__(self, name: str = 'llama-3.3-70b-instruct'):
        self.name = name
        self.client = OpenAI(
            base_url=os.environ.get('BASE_URL', ''),
            api_key=os.environ.get('API_KEY', '')
        )

    def query(self, prompt: str) -> str:
        """Process the input prompt and return the model's response.

        Args:
            prompt: Input text prompt for the model.

        Returns:
            Model's response as a string.
        """
        response = self.client.chat.completions.create(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=int(os.environ.get('MAX_TOKENS', 75)),
            temperature=float(os.environ.get('TEMPERATURE', 0.0))
        )
        return response.choices[0].message.content
