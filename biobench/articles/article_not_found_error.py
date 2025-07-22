class ArticleNotFoundError(Exception):
    """Exception raised when article with specified DOI is not found."""
    def __init__(self, doi: str):
        self.doi = doi
        super().__init__(f"Article with DOI '{doi}' not found")