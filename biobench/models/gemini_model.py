import os

from google import genai
from google.genai import types

from biobench.ai_model import AIModel
from biobench.articles.pdf_articles_repo import PdfArticlesRepo


class GeminiModel(AIModel):
    def __init__(self, name: str = 'gemini-2.0-flash'):
        super().__init__(name)
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        self.articles_repo = PdfArticlesRepo()

    def query(self, prompt: str, article_ids: str) -> str:
        model = self.name

        parts = [types.Part.from_text(text=prompt)]

        for article_id in article_ids:
            article_bytes = self.articles_repo.get_article(article_id)

            parts.append(types.Part.from_bytes(data=article_bytes, mime_type="application/pdf"))

        contents = [
            types.Content(
                role="user",
                parts=parts,
            ),
        ]
        tools = [
            types.Tool(googleSearch=types.GoogleSearch(
            )),
        ]
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            response_mime_type="text/plain",
        )

        res = ''

        for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            res += chunk.text

        return res
