from biobench.assessments.db_assessments_repo import DbAssessmentsRepo
from biobench.tasks.task import Task


class CompleteAssessment:
    def __init__(self, id: str):
        self.id = id

    def result(self) -> float:
        pass


class Assessment:
    def __init__(self, id: str, repo: DbAssessmentsRepo):
        self.id = id
        self.repo = repo

    def save_score(self, task: Task, score: dict):
        self.repo.save_score(task.id, self.id, score)

    def complete(self) -> CompleteAssessment:
        self.repo.complete(self.id)
        return CompleteAssessment(self.id)