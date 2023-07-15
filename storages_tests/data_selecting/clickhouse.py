import pandas as pd
from random import choice

from service.clickhouse_utils import select_ids, time_execute
from service.config import REPEAT_TEST_COUNT, DATA_SELECTING_RESULT_FILE_NAME
from service.select_queries import QUERIES


def select_query_avr_time(query):
    return (
        sum(time_execute(QUERIES[query]["Clickhouse"], values) for _ in range(REPEAT_TEST_COUNT))
        # / REPEAT_TEST_COUNT
    )


def select_time_rate():
    try:
        test_results_df = pd.read_csv(DATA_SELECTING_RESULT_FILE_NAME)
    except FileNotFoundError:
        test_results_df = pd.DataFrame(index=QUERIES.keys())

    test_results_df = pd.merge(
        test_results_df,
        pd.DataFrame(
            [select_query_avr_time(query) for query in QUERIES],
            columns=["Clickhouse"],
            index=QUERIES.keys(),
        ),
        left_index=True,
        right_index=True,
    )
    test_results_df = test_results_df.round(4)
    test_results_df.to_csv(DATA_SELECTING_RESULT_FILE_NAME)


if __name__ == "__main__":
    users_ids = select_ids("user_id")
    movies_ids = select_ids("movie_id")
    values = {"user_id": choice(users_ids), "movie_id": choice(movies_ids)}
    select_time_rate()
