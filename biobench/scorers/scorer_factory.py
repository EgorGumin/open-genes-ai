from biobench.scorers.scorer import Scorer
from biobench.scorers.exact_scorer import ExactScorer
from biobench.scorers.scorer import ScoringModel


def get_scorer(scoring_model: ScoringModel) -> Scorer:
    if scoring_model == "Exact":
        return ExactScorer()
    else:
        raise ValueError(f"Scoring model {scoring_model} not supported")    