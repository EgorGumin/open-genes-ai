from abc import ABC, abstractmethod
from typing import List

from biobench.article import Article
from biobench.scorers.scorer_factory import get_scorer


class Task(ABC):
    def __init__(self, id: str, reference_solution: str, articles: List[Article]):
        self.id = id
        self.articles = articles
        self.reference_solution = reference_solution

    @abstractmethod
    def compile(self) -> str:
        pass

    def _compile_articles_block(self) -> str:
        text = ''
        for article in self.articles:
            text += f'<article doi="{article.doi}">{article.md_text}</article>\n'
        return text

    def score(self, solution: str) -> float:
        scorer = get_scorer(self.scoring_model)
        return scorer.score(solution, self.reference_solution)
