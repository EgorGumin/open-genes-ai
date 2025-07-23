from typing import List

from biobench.tasks.task import Task
from biobench.tasks.task_body_dto import ScoringConfig


class OpenEndedTask(Task):

    def __init__(
            self,
            id: str,
            reference_solution: str,
            article_ids: List[str],
            scoring_model: ScoringConfig,
            text: str
    ):
        super().__init__(id, reference_solution, scoring_model, article_ids, text)

    def compile(self) -> str:
        text = f'{self.text}'

        return text
