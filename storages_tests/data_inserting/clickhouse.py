import pandas as pd
from random import randint, choice

from data_filling.clickhouse import INSERT_QUERY
from service.clickhouse_utils import time_execute, select_ids
from service.config import CHUNKS, REPEAT_TEST_COUNT, DATA_INSERTING_RESULT_FILE_NAME


def insert_query_avr_time(chunk):
    return (
        sum(
            time_execute(
                INSERT_QUERY,
                [
                    (
                        choice(users_ids),
                        choice(movies_ids),
                        randint(10_000, 30_000),
                    )
                    for _ in range(chunk)
                ],
            )
            for _ in range(REPEAT_TEST_COUNT)
        )
        # / REPEAT_TEST_COUNT
    )


def insert_time_rate():
    try:
        test_results_df = pd.read_csv(DATA_INSERTING_RESULT_FILE_NAME, index_col=0)
    except FileNotFoundError:
        test_results_df = pd.DataFrame(index=CHUNKS)

    test_results_df = pd.merge(
        test_results_df,
        pd.DataFrame(
            [insert_query_avr_time(chunk) for chunk in CHUNKS],
            columns=["Clickhouse"],
            index=CHUNKS,
        ),
        left_index=True,
        right_index=True,
    )
    test_results_df = test_results_df.round(4)
    test_results_df.to_csv(DATA_INSERTING_RESULT_FILE_NAME)


if __name__ == "__main__":
    users_ids = select_ids("user_id")
    movies_ids = select_ids("movie_id")
    insert_time_rate()
