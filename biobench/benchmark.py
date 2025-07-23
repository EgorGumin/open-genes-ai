from ai_model import AIModel
from biobench.tasks.tasks_repo import TaskRepo
from biobench.tasks.task import Task


class Assessment:
    def __init__(self, id: str):
        self.id = id

    def save_score(self, task: Task, score: float):
        pass

    def complete(self):
        pass


class CompleteAssessment:
    def __init__(self, id: str):
        self.id = id

    def result(self) -> float:
        pass


class Benchmark:
    def __init__(self, model: AIModel, task_repo: TaskRepo, assessment: Assessment):
        self.model = model
        self.task_repo = task_repo
        self.assessment = assessment

    def run(self):
        while True:
            task = self.task_repo.next()
            if task is None:
                break
            solution = self.model.query(task.compile(), task.article_ids)
            score = task.score(solution)
            self.assessment.save_score(task, score.score)

        self.assessment.complete()
        complete_assessment = CompleteAssessment(self.assessment.id)
        print(complete_assessment.result())
