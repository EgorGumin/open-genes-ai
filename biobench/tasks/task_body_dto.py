from typing import Any, Dict, List, TypedDict

from biobench.tasks.task import ScoringModelName


class TaskBodyDto(TypedDict):
    articles: List[str]
    content: Dict[str, Any]
    scoringModel: ScoringModelName
