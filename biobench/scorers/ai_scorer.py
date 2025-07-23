import json
from typing import Optional

from biobench.ai_model import AIModel
from biobench.scorers.score_result import ScoreResult
from biobench.scorers.scorer import Scorer, ScoringModel
from biobench.tasks.task_body_dto import ScoringConfig


class AIScorer(Scorer):
    scoring_model: ScoringModel = "AI"

    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def score(self, solution: str, reference: str, text: str, scoring: Optional[ScoringConfig] = None) -> ScoreResult:
        instructions = ((
                            scoring[
                                'instructions'] if scoring else None) or
                        'Use the normalized F1 metric to assess the similarity of responses, as a result return json with the score field - the similarity value from 0 to 1 and the reason field - a brief description of the reason for this result')

        prompt = f"""
    {instructions}

    Task: {text}
    Reference: {reference}
    Model Answer: {solution}

    Respond with JSON: {{"score": float, "reason": "short explanation"}}
    """

        response = self.ai_model.query(prompt, [])

        result = json.loads(response.strip())

        score = max(0.0, min(1.0, float(result.get('score', 0.0))))
        reason = result.get('reason', 'No reason provided')

        return ScoreResult(score=score, reason=reason)
