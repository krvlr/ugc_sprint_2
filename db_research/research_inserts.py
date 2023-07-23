import pandas as pdd

from db_research.service.config import INSERTING_RESULT_FILE_NAME
from db_research.service.mongo_utils import (time_insert_likes,
                                             time_insert_reviews,
                                             time_insert_bookmarks)
from db_research.service.postgres_utils import (time_insert_likes_pg,
                                                time_insert_reviews_pg,
                                                time_insert_bookmarks_pg)

QUERIES_INSERT = {"Вставка лайков": {"Mongo": time_insert_likes,
                                     "Postgres": time_insert_likes_pg},
                  "Вставка ревью": {"Mongo": time_insert_reviews,
                                    "Postgres": time_insert_reviews_pg},
                  "Вставка закладок": {"Mongo": time_insert_bookmarks,
                                       "Postgres": time_insert_bookmarks_pg}}


def insert_time_rate():
    try:
        test_results_ins = pdd.read_csv(INSERTING_RESULT_FILE_NAME, index_col=0, header=0)
    except FileNotFoundError:
        test_results_ins = pdd.DataFrame(index=QUERIES_INSERT.keys())

    test_results_ins = pdd.merge(
        test_results_ins,
        pdd.DataFrame(
            [QUERIES_INSERT[query]['Mongo']() for query in QUERIES_INSERT],
            columns=["Mongo"],
            index=QUERIES_INSERT.keys(),
        ),
        left_index=True,
        right_index=True,
    )

    test_results_ins = pdd.merge(
        test_results_ins,
        pdd.DataFrame(
            [QUERIES_INSERT[query]['Postgres']() for query in QUERIES_INSERT],
            columns=["Postgres"],
            index=QUERIES_INSERT.keys(),
        ),
        left_index=True,
        right_index=True,
    )
    test_results_ins = test_results_ins.round(4)
    test_results_ins.to_csv(INSERTING_RESULT_FILE_NAME)


def run_inserts_tests():
    insert_time_rate()


if __name__ == "__main__":
    try:
        run_inserts_tests()
    except Exception as ex:
        print(f'Error {ex}')
