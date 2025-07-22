from ai_model import AIModel
from task_repo import TaskRepo
from task import Task

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
        for task in self.task_repo.next():
            solution = self.model.query(task.compile())
            score = task.evaluate(solution)
            self.assessment.save_score(task, score)

        self.assessment.complete()
        complete_assessment = CompleteAssessment(self.assessment.id)
        print(complete_assessment.result())