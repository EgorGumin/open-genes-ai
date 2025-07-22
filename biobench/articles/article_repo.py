from abc import abstractmethod, ABC

from biobench.articles.article import Article


class ArticleRepo(ABC):
    """Abstract base class for article repositories."""

    @abstractmethod
    def get_article(self, doi: str) -> Article:
        """
        Get article object by DOI.

        Args:
            doi: Unique article identifier

        Returns:
            Article: Article object

        Raises:
            ArticleNotFoundError: If article is not found
        """
        pass

    @abstractmethod
    def article_exists(self, doi: str) -> bool:
        """
        Check if article exists by DOI.

        Args:
            doi: Unique article identifier

        Returns:
            bool: True if article exists, False otherwise
        """
        pass

    @abstractmethod
    def list_available_articles(self) -> list[str]:
        """
        Get list of all available article DOIs.

        Returns:
            list[str]: List of available article DOIs
        """
        pass
