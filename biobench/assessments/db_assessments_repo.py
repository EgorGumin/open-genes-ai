from contextlib import contextmanager
from typing import List, Tuple, Optional

from psycopg2.extensions import cursor, connection
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
import json

from biobench.db.db import main_pool
from biobench.tasks.task import Task
from biobench.tasks.tasks_factory import get_task


class DbAssessmentsRepo:
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

    def save_score(self, task_id: str, assessment_id: str, result: dict) -> None:
        with self.get_cursor() as (cur, conn):
            cur.execute(
                """
                INSERT INTO complete_tasks (task_id, assessment_id, result)
                VALUES (%s, %s, %s)
                """,
                (task_id, assessment_id, json.dumps(result))
            )
            conn.commit()

    def complete(self, id: str):
        with self.get_cursor() as (cur, conn):
            cur.execute(
                """
                UPDATE assessments SET complete = TRUE WHERE id = %s
                """,
                (id,)
            )
            conn.commit()
        
