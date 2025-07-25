from biobench.assessments.assessment import Assessment
from biobench.assessments.db_assessments_repo import DbAssessmentsRepo
from biobench.benchmark import Benchmark
from biobench.models.open_ai_model import OpenAIModel
from biobench.tasks.db_tasks_repo import DbTasksRepo

assessment = Assessment('01984143-b248-73b5-9055-4127a1fec229', DbAssessmentsRepo())
task_repo = DbTasksRepo()
model = OpenAIModel()


bench = Benchmark(model, task_repo, assessment)

bench.run()
