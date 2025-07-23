from dataclasses import dataclass


@dataclass
class ScoreResult:
    score: float
    reason: str
