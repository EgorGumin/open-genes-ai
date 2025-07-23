import os
from typing import List

from openai import OpenAI

from biobench.ai_model import AIModel
from biobench.articles.md_articles_repo import MdArticlesRepo


class OpenAIModel(AIModel):
    def __init__(self, name: str = 'llama-3.3-70b-instruct'):
        super().__init__(name)
        self.client = OpenAI(
            base_url=os.environ.get('BASE_URL', ''),
            api_key=os.environ.get('API_KEY', '')
        )
        self.articles_repo = MdArticlesRepo()

    def query(self, prompt: str, article_ids: List[str]) -> str:
        messages = [{"role": "user", "content": prompt}]

        for article_id in article_ids:
            text = self.articles_repo.get_article(article_id)
            article_block = f'<article doi="{article_id}">{text}</article>\n'
            messages.append({"role": "user", "content": article_block})

        response = self.client.chat.completions.create(
            model=self.name,
            messages=messages,
            max_tokens=int(os.environ.get('MAX_TOKENS', 1024)),
            temperature=float(os.environ.get('TEMPERATURE', 0.0))
        )
        return response.choices[0].message.content
