from pathlib import Path

from biobench.articles.article_not_found_error import ArticleNotFoundError
from biobench.articles.article_repo import ArticleRepo


class PdfArticlesRepo(ArticleRepo):
    """File system implementation of ArticleRepository returning base64 encoded .pdf files."""

    def __init__(self, base_path: str = None):
        if base_path is None:
            current_path = Path(__file__).resolve()
            project_root = current_path

            while project_root.parent != project_root:
                if (project_root / "data").exists():
                    break
                project_root = project_root.parent

            self.base_path = project_root / "data" / "pdf"
        else:
            self.base_path = Path(base_path)

    def get_article_path(self, doi: str) -> Path:
        return self.base_path / (doi + ".pdf")

    def article_exists(self, doi: str) -> bool:
        return self.get_article_path(doi).exists()

    def load_article_content(self, doi: str) -> bytes:
        if not self.article_exists(doi):
            raise ArticleNotFoundError(doi)

        try:
            pdf_file_path = self.get_article_path(doi)
            with open(pdf_file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            raise ArticleNotFoundError(doi)
        except IOError as e:
            raise IOError(f"Error reading article file '{doi}': {e}")

    def get_article(self, doi: str) -> bytes:
        return self.load_article_content(doi)

    def list_available_articles(self) -> list[str]:
        if not self.base_path.exists():
            return []

        available_dois = []
        for item in self.base_path.iterdir():
            if item.is_file() and item.suffix.lower() == ".pdf":
                # Remove the .pdf extension
                available_dois.append(item.stem)

        return available_dois
