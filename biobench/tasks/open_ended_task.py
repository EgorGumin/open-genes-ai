from biobench.tasks.task import Task


class OpenEndedTask(Task):
    def compile(self) -> str:
        return f"Write a short summary of the task. It should be a single sentence."