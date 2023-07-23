import pandas as pd

from db_research.service.config import SELECTING_RESULT_FILE_NAME
from db_research.service.mongo_utils import (time_get_likes_user,
                                             time_count_likes_movie,
                                             time_get_bookmarks_user,
                                             time_avg_score)
from db_research.service.postgres_utils import (time_get_likes_user_pg,
                                                time_count_likes_movie_pg,
                                                time_get_bookmarks_user_pg,
                                                time_avg_score_pg)

QUERIES_SELECT = {"Список всех лайков пользователя": {"Mongo": time_get_likes_user,
                                                      "Postgres": time_get_likes_user_pg},
                  "Количество лайков фильма": {"Mongo": time_count_likes_movie,
                                               "Postgres": time_count_likes_movie_pg},
                  "Список закладок пользователя": {"Mongo": time_get_bookmarks_user,
                                                   "Postgres": time_get_bookmarks_user_pg},
                  "Средняя оценка фильма": {"Mongo": time_avg_score,
                                            "Postgres": time_avg_score_pg}}


def select_time_rate():
    try:
        test_results_df = pd.read_csv(SELECTING_RESULT_FILE_NAME)
    except FileNotFoundError:
        test_results_df = pd.DataFrame(index=QUERIES_SELECT.keys())

    test_results_df = pd.merge(
        test_results_df,
        pd.DataFrame(
            [QUERIES_SELECT[query]["Mongo"]() for query in QUERIES_SELECT],
            columns=["Mongo"],
            index=QUERIES_SELECT.keys(),
        ),
        left_index=True,
        right_index=True,
    )

    test_results_df = pd.merge(
        test_results_df,
        pd.DataFrame(
            [QUERIES_SELECT[query]["Postgres"]() for query in QUERIES_SELECT],
            columns=["Postgres"],
            index=QUERIES_SELECT.keys(),
        ),
        left_index=True,
        right_index=True,
    )
    test_results_df = test_results_df.round(4)
    test_results_df.to_csv(SELECTING_RESULT_FILE_NAME)


def run_selects_tests():
    select_time_rate()


if __name__ == "__main__":
    try:
        run_selects_tests()
    except Exception as ex:
        print(f'Error {ex}')
