import os
from typing import List

from openai import OpenAI

from biobench.ai_model import AIModel
from biobench.articles.md_articles_repo import MdArticlesRepo


class OpenAIModel(AIModel):
    def __init__(self, name: str = 'llama-3.3-70b-instruct', params: dict = None):
        super().__init__(name)
        self.client = OpenAI(
            base_url=os.environ.get('BASE_URL', ''),
            api_key=os.environ.get('API_KEY', '')
        )
        self.articles_repo = MdArticlesRepo()
        self.params = params or {}

    def query(self, prompt: str, article_ids: List[str]) -> str:
        messages = [{"role": "user", "content": self.get_base_prompt()}]

        for article_id in article_ids:
            text = self.articles_repo.get_article(article_id)
            article_block = f'<article doi="{article_id}">{text}</article>\n'
            messages.append({"role": "user", "content": article_block})

            sups = self.articles_repo.get_supplementary(article_id)
            for sup in sups:
                sup_block = f'<supplementary doi="{article_id}" name="{sup['filename']}">{sup['content']}</supplementary>\n'
                messages.append({"role": "user", "content": sup_block})


        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.name,
            messages=messages,
            max_tokens=self.params.get('max_tokens', 128),
            temperature=self.params.get('temperature', 0)
        )
        return response.choices[0].message.content
