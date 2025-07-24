from abc import ABC, abstractmethod
from typing import List

from biobench.scorers.scorer_factory import get_scorer
from biobench.tasks.task_body_dto import ScoringConfig


class Task(ABC):
    def __init__(
            self,
            id: str,
            reference_solution: str,
            scoring: ScoringConfig,
            article_ids: List[str],
            text: str
    ):
        self.id = id
        self.article_ids = article_ids
        self.reference_solution = reference_solution
        self.scoring = scoring
        self.text = text

    @abstractmethod
    def compile(self) -> str:
        pass

    def score(self, solution: str) -> dict:
        scorer = get_scorer(self.scoring['model'])
        return scorer.score(solution, self.reference_solution, self.text, self.scoring)
