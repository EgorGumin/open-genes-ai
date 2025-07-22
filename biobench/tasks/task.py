from abc import ABC, abstractmethod

from biobench.article import Article


class Task(ABC):
    def __init__(self, id: str, articles: [Article]):
        self.id = id
        self.articles = articles

    @abstractmethod
    def compile(self) -> str:

        pass

    @abstractmethod
    def evaluate(self, solution: str) -> float:

        pass
