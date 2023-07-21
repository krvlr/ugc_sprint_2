import random
from random import randint

from service.config import timeit, user_ids, movie_ids, \
    COUNT_OF_SELECTS, \
    COUNT_OF_INSERTS
from service.mongo_utils import fill_mongo, research_inserts_mongo, \
    get_mongo_objects
from service.postgres_utils import research_inserts_pg, select_objects_pg, \
    fill_postgres_db

tables_names = ['likes',
                'reviews',
                'bookmarks']


@timeit
def fill_dbs_mongo():
    fill_mongo()


@timeit
def fill_dbs_pg():
    fill_postgres_db()


#
# def research_mongo_inserts(total_size, chunk_size):
#     research_inserts_mongo(total_size, chunk_size)


@timeit
def research_inserts_m_t():
    for j in range(COUNT_OF_INSERTS):
        chunk_size = 100000  # random.choice(CHUNKS)
        total_size = 200000  #randint(10000, 50000)
        research_inserts_mongo(total_size, chunk_size)


@timeit
def research_inserts_pg_t():
    for j in range(COUNT_OF_INSERTS):
        chunk_size = 100000  # random.choice(CHUNKS)
        total_size = 200000 #randint(10000, 50000)
        research_inserts_pg(total_size, chunk_size)


def research_select_mongo():
    for table in tables_names:
        for i in range(COUNT_OF_SELECTS):
            query_mongo = random.choice([{'user_id': random.choice(user_ids)},
                                         {'movie_id': random.choice(movie_ids)}])
            get_mongo_objects(table, query_mongo)


def research_select_pg():
    for table in tables_names:
        for i in range(COUNT_OF_SELECTS):
            query_pg = random.choice([{'user_id': random.choice(user_ids)},
                                      {'movie_id': random.choice(movie_ids)}])
            select_objects_pg(table, query_pg)


@timeit
def research_selects_m_t():
    research_select_mongo()


@timeit
def research_selects_pg_t():
    research_select_pg()


def run_perf_tests():
    print('Filling db')
    fill_dbs_mongo()
    fill_dbs_pg()
    print('DB filled')

    for i in range(3):
        print('Start mongo test')
        research_inserts_m_t()
        research_selects_m_t()
        print('Done mongo test')

        print('Start pg test')
        research_inserts_pg_t()
        research_selects_pg_t()
        print('Done pg test')


if __name__ == "__main__":
    try:
        run_perf_tests()
    except Exception as ex:
        print(f'Error {ex}')
