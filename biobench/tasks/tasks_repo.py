from abc import ABC, abstractmethod
from typing import Optional

from biobench.tasks.task import Task


class TaskRepo(ABC):
    @abstractmethod
    def next(self) -> Optional[Task]:
        pass
