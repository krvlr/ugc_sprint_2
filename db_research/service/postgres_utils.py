import datetime
import random
import uuid
from contextlib import closing
from time import time

import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from psycopg2.sql import Composed

from db_research.service.config import (
    perf_settings,
    user_ids,
    movie_ids,
    INIT_RECORDS_ALL,
    INIT_RECORDS_CHUNK,
    COUNT_OF_SELECTS,
)


def create_db():
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS events")
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS events.likes (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        like_score INT,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS events.reviews (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        review text,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS events.bookmarks (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )"""
            )

            cursor.execute("""TRUNCATE events.likes, events.reviews, events.bookmarks""")

            conn.commit()


def get_query_insert_likes():
    return "INSERT INTO events.likes (id, user_id, movie_id, like_score, created_at, updated_at) VALUES %s"


def get_query_insert_reviews():
    return "INSERT INTO events.reviews (id, user_id, movie_id, review, created_at, updated_at) VALUES %s"


def get_query_insert_bookmarks():
    return "INSERT INTO events.bookmarks (id, user_id, movie_id, created_at, updated_at) VALUES %s"


def get_query_select_likes():
    return "SELECT * FROM events.likes WHERE {param}=%s"


def get_query_select_reviews():
    return "SELECT * FROM events.reviews WHERE {param}=%s"


def get_query_select_bookmarks():
    return "SELECT * FROM events.bookmarks WHERE {param}=%s"


def get_query_count_likes():
    return "SELECT COUNT(*) FROM events.likes WHERE {param}=%s"


def get_query_avg_likes():
    return "SELECT AVG(like_score) FROM events.likes WHERE {param}=%s"


def generate_like_pg():
    return (
        str(uuid.uuid4()),
        random.choice(user_ids),
        random.choice(movie_ids),
        random.randint(0, 10),
        datetime.datetime.now(),
        datetime.datetime.now(),
    )


def generate_review_pg():
    user_id = random.choice(user_ids)
    movie_id = random.choice(movie_ids)
    return (
        str(uuid.uuid4()),
        user_id,
        movie_id,
        f"Review of {movie_id} from {user_id}",
        datetime.datetime.now(),
        datetime.datetime.now(),
    )


def generate_bookmark_pg():
    return (
        str(uuid.uuid4()),
        random.choice(user_ids),
        random.choice(movie_ids),
        datetime.datetime.now(),
        datetime.datetime.now(),
    )


def generate_chunk(chunk_size: int, generate_obj):
    return [generate_obj() for _ in range(chunk_size)]


generate_funcs = {
    "likes": generate_like_pg,
    "reviews": generate_review_pg,
    "bookmarks": generate_bookmark_pg,
}

queries_insert = {
    "likes": get_query_insert_likes(),
    "reviews": get_query_insert_reviews(),
    "bookmarks": get_query_insert_bookmarks(),
}

queries_select = {
    "likes": get_query_select_likes(),
    "reviews": get_query_select_reviews(),
    "bookmarks": get_query_select_bookmarks(),
}


def insert_chunk_pg(total_size: int, chunk_size: int, table_name: str):
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            inserted = 0
            insert_query = queries_insert[table_name]
            while inserted < total_size:
                input_data = generate_chunk(chunk_size, generate_funcs[table_name])
                psycopg2.extras.execute_values(
                    cursor, insert_query, input_data, template=None, page_size=chunk_size
                )
                conn.commit()
                inserted += chunk_size


def fill_postgres_db():
    print("Started filling pg")
    start = time()
    create_db()
    for table_name, gener_func in generate_funcs.items():
        insert_chunk_pg(INIT_RECORDS_ALL, INIT_RECORDS_CHUNK, table_name)
    print("Filling pg time ", round(time() - start, 4))


def time_execute_pg(
    cursor: DictCursor,
    query: str | Composed,
    values: list | dict | tuple | None = None,
    insert=False,
) -> float:
    start = time()
    if insert:
        psycopg2.extras.execute_values(cursor, query, values, template=None, page_size=10000)
    else:
        if values:
            cursor.execute(query, values)
            cursor.fetchall()
        else:
            cursor.execute(query)
            cursor.fetchall()
    return round(time() - start, 8)


def time_get_likes_user_pg():
    user_id = random.choice(user_ids)
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            select_query = queries_select["likes"]
            sql_comm = sql.SQL(select_query).format(param=sql.Identifier("user_id"))
            data = (user_id,)
            sum_time = sum(
                (time_execute_pg(cursor, sql_comm, data)) for _ in range(COUNT_OF_SELECTS)
            )
            print("pg likes of user time", sum_time)
            return sum_time


def time_count_likes_movie_pg():
    movie_id = random.choice(movie_ids)
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            count_query = get_query_count_likes()
            sql_comm = sql.SQL(count_query).format(param=sql.Identifier("movie_id"))
            data = (movie_id,)
            sum_time = time_execute_pg(cursor, sql_comm, data)
            print("pg count likes of movie time", sum_time)
            return sum_time


def time_get_bookmarks_user_pg():
    user_id = random.choice(user_ids)
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            select_query = queries_select["bookmarks"]
            sql_comm = sql.SQL(select_query).format(param=sql.Identifier("user_id"))
            data = (user_id,)
            sum_time = sum(
                (time_execute_pg(cursor, sql_comm, data)) for _ in range(COUNT_OF_SELECTS)
            )
            print("pg bookmarks of user time", sum_time)
            return sum_time


def time_avg_score_pg():
    movie_id = random.choice(movie_ids)
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            avg_query = get_query_avg_likes()
            sql_comm = sql.SQL(avg_query).format(param=sql.Identifier("movie_id"))
            data = (movie_id,)
            sum_time = time_execute_pg(cursor, sql_comm, data)
            print("pg avg score time", sum_time)
            return sum_time


def time_insert_likes_pg():
    chunk_likes = generate_chunk(INIT_RECORDS_CHUNK, generate_funcs["likes"])
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            insert_query = queries_insert["likes"]
            sum_time = time_execute_pg(cursor, insert_query, chunk_likes, insert=True)
            print("pg insert likes", sum_time)
            return sum_time


def time_insert_reviews_pg():
    chunk_reviews = generate_chunk(INIT_RECORDS_CHUNK, generate_funcs["reviews"])
    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            insert_query = queries_insert["reviews"]
            sum_time = time_execute_pg(cursor, insert_query, chunk_reviews, insert=True)
            print("pg insert reviews", sum_time)
            return sum_time


def time_insert_bookmarks_pg():
    chunk_bookmarks = generate_chunk(INIT_RECORDS_CHUNK, generate_funcs["bookmarks"])

    with closing(
        psycopg2.connect(
            dbname=perf_settings.dbname,
            user=perf_settings.username,
            password=perf_settings.password,
            host=perf_settings.host,
        )
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            insert_query = queries_insert["bookmarks"]
            sum_time = time_execute_pg(cursor, insert_query, chunk_bookmarks, insert=True)
            print("pg insert bookmarks", sum_time)
            return sum_time


if __name__ == "__main__":
    try:
        # fill_postgres_db()
        time_insert_likes_pg()
        # time_insert_reviews_pg()
        # time_insert_bookmarks_pg()
        # time_get_likes_user_pg()
        time_count_likes_movie_pg()
        # time_get_bookmarks_user_pg()
        # time_avg_score_pg()
    except Exception as ex:
        print(f"Error {ex}")
