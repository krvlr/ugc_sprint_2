QUERIES = {
    "Список всех фильмов пользователя": {
        "Clickhouse": """
            SELECT DISTINCT (movie_id)
            FROM research.views
            WHERE user_id = %(user_id)s
        """,
        "Vertica": """
            SELECT DISTINCT (movie_id)
            FROM views
            WHERE user_id = :user_id
        """,
        "has_params": True,
    },
    "Все фильмы пользователя с наибольшим временем просмотра": {
        "Clickhouse": """
            SELECT movie_id, max(timestamp)
            FROM research.views
            WHERE user_id = %(user_id)s
            GROUP BY movie_id
        """,
        "Vertica": """
            SELECT movie_id, max(timestamp)
            FROM views
            WHERE user_id = :user_id
            GROUP BY movie_id
        """,
        "has_params": True,
    },
    "Самый продолжительный просмотра фильма пользователем": {
        "Clickhouse": """
            SELECT max(timestamp)
            FROM research.views
            WHERE movie_id = %(movie_id)s AND user_id = %(user_id)s
        """,
        "Vertica": """
            SELECT max(timestamp)
            FROM views
            WHERE movie_id = :movie_id AND user_id = :user_id
        """,
        "has_params": True,
    },
    "Список пользователей смотревших фильм": {
        "Clickhouse": """
            SELECT DISTINCT user_id
            FROM research.views
            WHERE movie_id = %(movie_id)s
        """,
        "Vertica": """
            SELECT DISTINCT user_id
            FROM views
            WHERE movie_id = :movie_id
        """,
        "has_params": True,
    },
    "Запрос общего количества записей": {
        "Clickhouse": "SELECT count() FROM research.views",
        "Vertica": "SELECT count(*) FROM views",
        "has_params": False,
    },
    "Среднее время просмотра каждого фильма": {
        "Clickhouse": """
            SELECT movie_id, avg(timestamp)
            FROM research.views
            GROUP BY movie_id
        """,
        "Vertica": """
            SELECT movie_id, avg(timestamp)
            FROM views
            GROUP BY movie_id
        """,
        "has_params": False,
    },
    "Список всех пользователей": {
        "Clickhouse": "SELECT DISTINCT user_id from research.views",
        "Vertica": "SELECT DISTINCT user_id from views",
        "has_params": False,
    },
    "Количество запусков просмотра": {
        "Clickhouse": """
            SELECT user_id, count(movie_id)
            FROM research.views
            GROUP BY user_id
        """,
        "Vertica": """
            SELECT user_id, count(movie_id)
            FROM views
            GROUP BY user_id
        """,
        "has_params": False,
    },
}
