from contextlib import contextmanager
from typing import List, Tuple, Optional

from psycopg2.extensions import cursor, connection
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from biobench.db.db import main_pool
from biobench.tasks.task import Task
from biobench.tasks.tasks_factory import get_task
from biobench.tasks.tasks_repo import TaskRepo


class DbTasksRepo(TaskRepo):
    def __init__(self, db_pool: ThreadedConnectionPool = main_pool):
        self.db_pool = db_pool
        self._task_ids: List[str] = []
        self._current_task_index = 0

    @contextmanager
    def get_cursor(self) -> Tuple[RealDictCursor, connection]:
        conn = self.db_pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                yield cur, conn
        finally:
            self.db_pool.putconn(conn)

    def _get_task_ids(self) -> List[str]:
        with self.get_cursor() as (cur, conn):
            cur: cursor
            cur.execute("""
                SELECT id 
                FROM tasks 
                ORDER BY "id" ASC
            """)
            return [row["id"] for row in cur.fetchall()]

    def _get_task(self, id: str) -> Task:
        with self.get_cursor() as (cur, conn):
            cur: cursor
            cur.execute("""
                SELECT id, body
                FROM tasks 
                WHERE id = %s
            """, (id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Task with id {id} not found")
            return get_task(row["id"], row["body"])

    def next(self) -> Optional[Task]:
        if len(self._task_ids) == 0:
            self._task_ids = self._get_task_ids()

        index = self._current_task_index
        if index < len(self._task_ids):
            self._current_task_index += 1
            return self._get_task(self._task_ids[index])
        return None
