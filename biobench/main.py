from biobench.articles.article_not_found_error import ArticleNotFoundError
from biobench.articles.md_articles_repo import FileSystemArticleRepo

repo = FileSystemArticleRepo()

# Example usage with exception handling
try:
    article = repo.get_article("10.1234/example.doi")
    print(f"Loaded article with DOI: {article.doi}")
    print(f"Content size: {len(article.md_text)} characters")
except ArticleNotFoundError as e:
    print(f"Error: {e}")
except IOError as e:
    print(f"IO Error: {e}")

# Safe article retrieval
article = repo.get_article("10.1001_jamanetworkopen.2018.1670")
if article:
    print("Article loaded successfully")
    print((article.md_text))
else:
    print("Article not found or error occurred")

# Check article existence
if repo.article_exists("10.1002_ana.22403"):
    print("Article exists")
else:
    print("Article not found")

# List available articles
available_articles = repo.list_available_articles()
print(f"Available articles: {available_articles}")
