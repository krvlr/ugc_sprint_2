from time import time


def select_users_ids(cursor) -> list[str]:
    cursor.execute("""SELECT DISTINCT user_id from views""")
    rows = cursor.fetchall()
    return ["".join(row) for row in rows]


def select_movies_ids(cursor) -> list[str]:
    cursor.execute("""SELECT DISTINCT movie_id from views""")
    rows = cursor.fetchall()
    return ["".join(row) for row in rows]


def time_execute(cursor, query: str, values: list | dict = None, insert=False) -> float:
    start = time()
    if insert:
        cursor.executemany(query, values, use_prepared_statements=False)
    else:
        if values:
            cursor.execute(query, values, use_prepared_statements=False)
        else:
            cursor.execute(query)
    return round(time() - start, 4)
