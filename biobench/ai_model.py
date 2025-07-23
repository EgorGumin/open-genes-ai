from abc import ABC, abstractmethod
from typing import List


class AIModel(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def query(self, prompt: str, article_ids: List[str]) -> str:
        pass
