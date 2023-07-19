import random
from random import randint

from service.config import timeit, CHUNKS, user_ids, movie_ids, COUNT_OF_SELECTS, \
    COUNT_OF_INSERTS
from service.mongo_utils import fill_mongo, research_inserts_mongo, \
    get_mongo_objects

tables_names = ['likes',
                'reviews',
                'bookmarks']


@timeit
def fill_dbs():
    fill_mongo()


def research_mongo_inserts(total_size, chunk_size):
    research_inserts_mongo(total_size, chunk_size)


@timeit
def research_inserts():
    for j in range(COUNT_OF_INSERTS):
        chunk_size = 10000 #random.choice(CHUNKS)
        total_size = randint(10000, 50000)
        research_mongo_inserts(total_size, chunk_size)


def research_select_mongo():
    for table in tables_names:
        for i in range(COUNT_OF_SELECTS):
            query_mongo = random.choice([{'user_id': random.choice(user_ids)},
                                        {'movie_id': random.choice(movie_ids)}])
            get_mongo_objects(table, query_mongo)


@timeit
def research_selects():
    research_select_mongo()


def run_perf_tests():
    print('Start')
    fill_dbs()
    research_inserts()
    research_selects()
    print('Done')


if __name__ == "__main__":
    run_perf_tests()
