import pandas as pd
import vertica_python
from random import choice

from data_filling.vertica import CONNECTION_CONFIG
from service.config import REPEAT_TEST_COUNT, DATA_SELECTING_RESULT_FILE_NAME
from service.select_queries import QUERIES
from service.vertica_utils import select_users_ids, select_movies_ids, time_execute


def select_query_avr_time(query):
    return (
        sum(
            time_execute(
                cursor,
                query=QUERIES[query]["Vertica"],
                values=values if QUERIES[query]["has_params"] else None,
            )
            for _ in range(REPEAT_TEST_COUNT)
        )
        # / REPEAT_TEST_COUNT
    )


def select_time_rate():
    try:
        test_results_df = pd.read_csv(DATA_SELECTING_RESULT_FILE_NAME, index_col=0)
    except FileNotFoundError:
        test_results_df = pd.DataFrame(index=QUERIES.keys())

    test_results_df = pd.merge(
        test_results_df,
        pd.DataFrame(
            [select_query_avr_time(query) for query in QUERIES],
            columns=["Vertica"],
            index=QUERIES.keys(),
        ),
        left_index=True,
        right_index=True,
    )
    test_results_df = test_results_df.round(4)
    test_results_df.to_csv(DATA_SELECTING_RESULT_FILE_NAME)


if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_CONFIG) as connection:
        cursor = connection.cursor()

        values = {
            "user_id": choice(select_users_ids(cursor)),
            "movie_id": choice(select_movies_ids(cursor)),
        }
        select_time_rate()
