import glob
import json
import os
import mysql.connector

from uuid6 import uuid7

from biobench.db.db import put_db_connection, get_db_connection


def read_queries(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    queries = [q.strip() for q in content.split('\n\n') if q.strip()]

    if len(queries) == 1:
        queries = [q.strip() for q in content.split(';') if q.strip()]

    return queries


def execute_mysql_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def insert_to_postgres(cursor, data):
    if not data:
        return

    for row in data:
        task_id = str(uuid7())

        if isinstance(row, dict) and 'body' in row:
            body_content = json.loads(row['body']) if isinstance(row['body'], str) else row['body']
            cursor.execute("INSERT INTO public.tasks (id, body) VALUES (%s, %s)", (task_id, body_content))
        else:
            cursor.execute("INSERT INTO public.tasks (id, body) VALUES (%s, %s)", (task_id, row))


def main():
    sql_queries = read_queries('generator.sql')

    json_data = []
    json_files = glob.glob("*.json")  # все JSON файлы в текущей папке

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            json_data.append(data)

    postgres_conn = get_db_connection()
    postgres_cursor = postgres_conn.cursor()

    try:
        if sql_queries:
            mysql_conn = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST", "localhost"),
                user=os.environ.get("MYSQL_USER", ""),
                password=os.environ.get("MYSQL_PASSWORD", ""),
                database=os.environ.get("MYSQL_DATABASE", "opengenes")
            )

            mysql_cursor = mysql_conn.cursor(dictionary=True)

            try:
                for query in sql_queries:
                    mysql_results = execute_mysql_query(mysql_cursor, query)
                    insert_to_postgres(postgres_cursor, mysql_results)
            finally:
                mysql_cursor.close()
                mysql_conn.close()

        if json_data:
            insert_to_postgres(postgres_cursor, json_data)

        postgres_conn.commit()
        print(f"Обработано {len(sql_queries)} SQL запросов и {len(json_data)} JSON файлов")

    finally:
        postgres_cursor.close()
        put_db_connection(postgres_conn)


if __name__ == "__main__":
    main()
