from biobench.ai_model import AIModel
from biobench.models.open_ai_model import OpenAIModel
from biobench.scorers.ai_scorer import AIScorer
from biobench.scorers.scorer import Scorer
from biobench.scorers.exact_scorer import ExactScorer
from biobench.scorers.scorer import ScoringModel


def get_scorer(scoring_model: ScoringModel, ai_model: AIModel = None) -> Scorer:
    if scoring_model == "Exact":
        return ExactScorer()
    elif scoring_model == "AI":
        if ai_model is None:
            # Use default OpenAI model if none provided
            ai_model = OpenAIModel()
        return AIScorer(ai_model)
    else:
        raise ValueError(f"Scoring model {scoring_model} not supported")    