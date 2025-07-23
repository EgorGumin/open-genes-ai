from biobench.benchmark import Assessment, Benchmark
from biobench.models.gemini_model import GeminiModel
from biobench.models.open_ai_model import OpenAIModel
from biobench.tasks.db_tasks_repo import DbTasksRepo

assessment = Assessment("test")
task_repo = DbTasksRepo()
# model = OpenAIModel()
model = GeminiModel()


bench = Benchmark(model, task_repo, assessment)

bench.run()