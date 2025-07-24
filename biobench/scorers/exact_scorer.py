from typing import Optional

from biobench.scorers.scorer import Scorer, ScoringModel
from biobench.tasks.task_body_dto import ScoringConfig


class ExactScorer(Scorer):
    scoring_model: ScoringModel = "Exact"

    def score(self, solution: str, reference: str, text: str, scoring: Optional[ScoringConfig] = None) -> dict:
        print(f"{solution} \n\n {reference}")
        is_match = solution.lower().strip() == reference.lower().strip()
        return {
            "score": 1.0 if is_match else 0.0,
            "reason": "Exact match" if is_match else "Does not match exactly"
        }
