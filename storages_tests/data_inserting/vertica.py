from random import randint, choice

import pandas as pd
import vertica_python

from data_filling.vertica import CONNECTION_CONFIG
from data_filling.vertica import INSERT_QUERY
from service.config import CHUNKS, REPEAT_TEST_COUNT, DATA_INSERTING_RESULT_FILE_NAME
from service.vertica_utils import select_users_ids, select_movies_ids, time_execute


def insert_query_avr_time(chunk):
    return (
        sum(
            time_execute(
                cursor,
                INSERT_QUERY,
                [
                    (
                        choice(users_ids),
                        choice(movies_ids),
                        randint(10_000, 30_000),
                    )
                    for _ in range(chunk)
                ],
                insert=True,
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
            columns=["Vertica"],
            index=CHUNKS,
        ),
        left_index=True,
        right_index=True,
    )
    test_results_df = test_results_df.round(4)
    test_results_df.to_csv(DATA_INSERTING_RESULT_FILE_NAME)


if __name__ == "__main__":
    with vertica_python.connect(**CONNECTION_CONFIG) as connection:
        cursor = connection.cursor()
        users_ids = select_users_ids(cursor)
        movies_ids = select_movies_ids(cursor)
        insert_time_rate()
