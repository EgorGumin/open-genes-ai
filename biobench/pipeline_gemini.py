from biobench.assessments.assessment import Assessment
from biobench.assessments.db_assessments_repo import DbAssessmentsRepo
from biobench.benchmark import Benchmark
from biobench.models.gemini_model import GeminiModel
from biobench.tasks.db_tasks_repo import DbTasksRepo

assessment = Assessment('01983caf-daa1-7716-9155-61257bddfb6c', DbAssessmentsRepo())
task_repo = DbTasksRepo()
model = GeminiModel()


bench = Benchmark(model, task_repo, assessment)

bench.run()
