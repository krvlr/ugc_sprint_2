import datetime
import random
import uuid
from contextlib import closing

import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

from db_research.service.config import perf_settings, user_ids, movie_ids, \
    timeit, INIT_RECORDS_ALL, INIT_RECORDS_CHUNK


def create_db():
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('CREATE SCHEMA IF NOT EXISTS events')
            cursor.execute('''CREATE TABLE IF NOT EXISTS events.likes (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        like_score INT,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS events.reviews (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        review text,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS events.bookmarks (id uuid PRIMARY KEY,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

            cursor.execute('''TRUNCATE events.likes, events.reviews, events.bookmarks''')

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
    return "SELECT * FROM events.reviews WHERE %s=%s"


def get_query_select_bookmarks():
    return "SELECT * FROM events.bookmarks WHERE %s=%s"


def generate_like_pg():
    return (str(uuid.uuid4()), random.choice(user_ids), random.choice(movie_ids),
            random.randint(0, 10), datetime.datetime.now(),
            datetime.datetime.now())


def generate_review_pg():
    user_id = random.choice(user_ids)
    movie_id = random.choice(movie_ids)
    return (str(uuid.uuid4()), user_id, movie_id,
            f'Review of {movie_id} from {user_id}', datetime.datetime.now(),
            datetime.datetime.now())


def generate_bookmark_pg():
    return (str(uuid.uuid4()), random.choice(user_ids), random.choice(movie_ids),
            datetime.datetime.now(), datetime.datetime.now())


def generate_chunk(chunk_size: int, generate_obj):
    return [generate_obj() for _ in range(chunk_size)]


generate_funcs = {'likes': generate_like_pg,
                  'reviews': generate_review_pg,
                  'bookmarks': generate_bookmark_pg}

queries_insert = {'likes': get_query_insert_likes(),
                  'reviews': get_query_insert_reviews(),
                  'bookmarks': get_query_insert_bookmarks()}

queries_select = {'likes': get_query_select_likes(),
                  'reviews': get_query_select_reviews(),
                  'bookmarks': get_query_select_bookmarks()}


def insert_chunk_pg(total_size: int, chunk_size: int, table_name: str):
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            inserted = 0
            insert_query = queries_insert[table_name]
            print(insert_query)
            while inserted < total_size:
                input_data = generate_chunk(chunk_size, generate_funcs[table_name])
                psycopg2.extras.execute_values(
                    cursor, insert_query, input_data, template=None, page_size=chunk_size)
                conn.commit()
                inserted += chunk_size


def select_objects_pg(table_name: str, params: dict):
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            select_query = queries_select[table_name]

            param = list(params.items())[0]
            sql_comm = sql.SQL(select_query).format(param=sql.Identifier(param[0]))
            cursor.execute(sql_comm, (param[1],))
            rows = cursor.fetchall()
            print(len(rows))
            return rows


def research_inserts_pg(total_records_per_table, chunk_size):
    for table_name, gener_func in generate_funcs.items():
        insert_chunk_pg(total_records_per_table, chunk_size, table_name)


@timeit
def fill_postgres_db(total_size: int, chunk_size: int):
    insert_chunk_pg(total_size, chunk_size, 'likes')
    insert_chunk_pg(total_size, chunk_size, 'reviews')
    insert_chunk_pg(total_size, chunk_size, 'bookmarks')


if __name__ == "__main__":
    try:
        # start_time = time.perf_counter()
        create_db()
        fill_postgres_db(INIT_RECORDS_ALL, INIT_RECORDS_CHUNK)
        select_objects_pg('likes', {'like_score': 1})
        # end_time = time.perf_counter()
        # total_time = end_time - start_time
        # print(f'Took {total_time:.4f} seconds')
    except Exception as ex:
        print(f'Error {ex}')
