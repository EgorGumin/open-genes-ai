from abc import ABC, abstractmethod
from typing import Literal, Optional

from biobench.tasks.task_body_dto import ScoringConfig

ScoringModel = Literal["Exact", "AI"]


class Scorer(ABC):
    scoring_model: ScoringModel

    @abstractmethod
    def score(self, solution: str, reference: str, text: str, scoring: Optional[ScoringConfig] = None) -> dict:
        pass
