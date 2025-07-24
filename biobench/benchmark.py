from ai_model import AIModel
from biobench.assessments.assessment import Assessment, CompleteAssessment
from biobench.tasks.tasks_repo import TaskRepo


class Benchmark:
    def __init__(self, model: AIModel, task_repo: TaskRepo, assessment: Assessment):
        self.model = model
        self.task_repo = task_repo
        self.assessment = assessment

    def run(self):
        while True:
            task = self.task_repo.next(self.assessment.id)
            if task is None:
                break
            print(task.id)
            solution = self.model.query(task.compile(), task.article_ids)
            score = task.score(solution)
            print(score)
            self.assessment.save_score(task, score)

        complete_assessment = self.assessment.complete()
        print(complete_assessment.result())
