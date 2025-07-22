from abc import ABC, abstractmethod

from typing import Literal

ScoringModel = Literal["Exact"]

class Scorer(ABC):
    scoring_model: ScoringModel

    @abstractmethod
    def score(self, solution: str, reference: str) -> float:
        pass