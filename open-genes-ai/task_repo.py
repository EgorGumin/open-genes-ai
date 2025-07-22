from abc import ABC, abstractmethod
from typing import Iterator

from task import Task


class TaskRepo(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def next(self) -> Iterator[Task]:
        pass
