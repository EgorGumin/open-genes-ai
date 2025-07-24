from asyncio import Task

from biobench.tasks.open_ended_task import OpenEndedTask
from biobench.tasks.task_body_dto import TaskBodyDto


def get_task(id: str, body: TaskBodyDto) -> Task:

    if body['content']['type'] is not None:
        return OpenEndedTask(id, body['content']['referenceSolution'], body['articles'], body['scoring'],
                             body['content']['text'])

    raise ValueError(f"Task type {body['content']['type']} not supported")
