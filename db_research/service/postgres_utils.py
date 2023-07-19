import random
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

from db_research.service.config import perf_settings, generate_like, user_ids


def create_db():
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('CREATE SCHEME IF NOT EXISTS events')
            cursor.execute('''CREATE TABLE IF NOT EXISTS events.likes (ID INT PRIMARY KEY NOT NULL,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        like int,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS events.reviews (ID INT PRIMARY KEY NOT NULL,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        review text,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS events.bookmarks (ID INT PRIMARY KEY NOT NULL,
                                                                        user_id uuid NOT NULL,
                                                                        movie_id uuid NOT NULL,
                                                                        created_at timestamp,
                                                                        updated_at timestamp
                                                                        )''')

#
# query = sql.SQL("INSERT INTO {table}({cols}) values %s")\
# .format(table=sql.Identifier(schema, table),
#         cols=sql.SQL(", ").join(map(sql.Identifier, col_lst)))

def insert_postgr_obj():
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            data = generate_like()
            insert_query = "INSERT INTO events.likes (user_id, movie_id, like, created_at, updated_at) VALUES %s"
            psycopg2.extras.execute_values(
                cursor, insert_query, list(data.values()), template=None, page_size=100
            )
            conn.commit()

def select_postgr_obj():
    with closing(psycopg2.connect(dbname=perf_settings.dbname,
                                  user=perf_settings.username,
                                  password=perf_settings.password,
                                  host=perf_settings.host)) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            user_id=random.choice(user_ids)
            select_query = "SELECT * FROM events.likes WHERE user_id=%s"
            cursor.execute(select_query, (user_id,))
            cursor.fetchmany(100)

