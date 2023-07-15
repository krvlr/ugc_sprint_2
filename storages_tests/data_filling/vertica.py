import vertica_python
from tqdm import tqdm

from service.config import (
    generate_views,
    INIT_RECORDS_CHUNK,
    INIT_RECORDS_ALL,
)

CONNECTION_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "VMart",
    "autocommit": True,
}

INSERT_QUERY = """INSERT INTO views (user_id, movie_id, timestamp) VALUES (%s,%s, %s)"""


def init_db(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS views (
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            timestamp INTEGER NOT NULL
        )
        ORDER BY user_id, movie_id;
        """
    )


def fill_db(cursor, chunk: int = INIT_RECORDS_CHUNK, total_size: int = INIT_RECORDS_ALL):
    for _ in tqdm(range(1, total_size, chunk), desc="Запись в Vertica"):
        cursor.executemany(
            INSERT_QUERY,
            generate_views(chunk),
            use_prepared_statements=False,
        )


if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_CONFIG) as connection:
        cursor = connection.cursor()
        init_db(cursor)
        fill_db(cursor)
