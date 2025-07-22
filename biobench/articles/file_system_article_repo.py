from pathlib import Path

from biobench.articles.article import Article
from biobench.articles.article_not_found_error import ArticleNotFoundError
from biobench.articles.article_repo import ArticleRepo


class FileSystemArticleRepo(ArticleRepo):
    """File system implementation of ArticleRepository."""

    def __init__(self, base_path: str = None):
        if base_path is None:
            current_path = Path(__file__).resolve()
            project_root = current_path

            while project_root.parent != project_root:
                if (project_root / "data").exists():
                    break
                project_root = project_root.parent

            self.base_path = project_root / "data" / "PDF_DIR"
        else:
            self.base_path = Path(base_path)

    def get_article_path(self, doi: str) -> Path:
        return self.base_path / doi

    def get_md_file_path(self, doi: str) -> Path:
        article_dir = self.get_article_path(doi)
        md_files = list(article_dir.glob("*.md"))
        if not md_files:
            raise FileNotFoundError(f"No .md file found in directory for DOI '{doi}'")
        return md_files[0]

    def article_exists(self, doi: str) -> bool:
        article_dir = self.get_article_path(doi)
        if not article_dir.exists() or not article_dir.is_dir():
            return False

        md_files = list(article_dir.glob("*.md"))
        return len(md_files) > 0

    def load_article_content(self, doi: str) -> str:
        if not self.article_exists(doi):
            raise ArticleNotFoundError(doi)

        try:
            md_file_path = self.get_md_file_path(doi)
            with open(md_file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise ArticleNotFoundError(doi)
        except IOError as e:
            raise IOError(f"Error reading article file '{doi}': {e}")

    def get_article(self, doi: str) -> Article:
        md_text = self.load_article_content(doi)
        return Article(doi=doi, md_text=md_text)

    def list_available_articles(self) -> list[str]:
        if not self.base_path.exists():
            return []

        available_dois = []
        for item in self.base_path.iterdir():
            if item.is_dir():
                # Check if directory contains .md files
                md_files = list(item.glob("*.md"))
                if md_files:
                    available_dois.append(item.name)

        return available_dois
