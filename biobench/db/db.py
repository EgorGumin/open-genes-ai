from psycopg2.pool import ThreadedConnectionPool
from os import environ

DATABASE_URL = environ.get("DATABASE_URL")

# Initialize main connection pool
main_pool = ThreadedConnectionPool(minconn=2, maxconn=5, dsn=DATABASE_URL)


def get_db_connection():
    """Get a database connection from the main pool"""
    return main_pool.getconn()


def put_db_connection(conn):
    """Return a connection to the main pool"""
    if conn:
        main_pool.putconn(conn)


def cleanup_pools():
    """Cleanup main database connection pool"""
    if main_pool:
        main_pool.closeall()
