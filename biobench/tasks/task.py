from abc import ABC, abstractmethod
from typing import List, Literal

from biobench.scorers.scorer_factory import get_scorer

ScoringModelName = Literal["Exact"]


class Task(ABC):
    def __init__(
            self,
            id: str,
            reference_solution: str,
            scoring_model: ScoringModelName,
            article_ids: List[str]
    ):
        self.id = id
        self.article_ids = article_ids
        self.reference_solution = reference_solution
        self.scoring_model = scoring_model

    @abstractmethod
    def compile(self) -> str:
        pass

    def score(self, solution: str) -> float:
        scorer = get_scorer(self.scoring_model)
        return scorer.score(solution, self.reference_solution)
