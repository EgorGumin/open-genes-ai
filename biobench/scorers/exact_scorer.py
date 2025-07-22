from biobench.scorers.scorer import Scorer, ScoringModel

class ExactScorer(Scorer):
    scoring_model: ScoringModel = "Exact"

    def score(self, solution: str, reference: str) -> float:
        return 1.0 if solution == reference else 0.0
