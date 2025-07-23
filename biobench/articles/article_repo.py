from abc import abstractmethod, ABC


class ArticleRepo(ABC):
    """Abstract base class for article repositories."""

    @abstractmethod
    def get_article(self, doi: str) -> str:
        """
        Get article object by DOI.

        Args:
            doi: Unique article identifier

        Returns:
            str: string representation of the article

        Raises:
            ArticleNotFoundError: If article is not found
        """
        pass

    @abstractmethod
    def article_exists(self, doi: str) -> bool:
        """
        Check if an article exists by DOI.

        Args:
            doi: Unique article identifier

        Returns:
            bool: True if the article exists, False otherwise
        """
        pass

    @abstractmethod
    def list_available_articles(self) -> list[str]:
        """
        Get a list of all available article DOIs.

        Returns:
            list[str]: List of available article DOIs
        """
        pass
