from typing import List
from biobench.article import Article
from biobench.tasks.task import Task


class OpenEndedTask(Task):

    def __init__(self, id: str, articles: List[Article], text: str):
        super().__init__(id, articles)
        self.text = text

    def compile(self) -> str:
        text = f'{self.text}\n\n{self._compile_articles_block()}'

        return text