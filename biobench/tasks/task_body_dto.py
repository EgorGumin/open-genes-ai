from typing import List, TypedDict, Optional, Literal

ScoringModelName = Literal["Exact", "AI"]


class ScoringConfig(TypedDict):
    model: ScoringModelName
    instructions: Optional[str]


class Content(TypedDict):
    text: str
    type: Literal["OpenEnded"]
    referenceSolution: str


class TaskBodyDto(TypedDict):
    articles: List[str]
    content: Content
    scoring: ScoringConfig
