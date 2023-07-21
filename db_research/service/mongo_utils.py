import time

from pymongo import MongoClient

from service.config import INIT_RECORDS_ALL, INIT_RECORDS_CHUNK, generate_like, \
    generate_review, generate_bookmark

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DB = "ugc_db"

mongo_cl = MongoClient('mongodb://localhost:27019/')
mongo_cl.drop_database('events')
mongo_db = mongo_cl.get_database('events')

gen_funcs = {'likes': generate_like,
             'reviews': generate_review,
             'bookmarks': generate_bookmark}


def generate_objects(chunk_size: int, gen_func) -> list:
    return [(gen_func()) for _ in range(chunk_size)]


def insert_mongo_objects(collection_name: str, gen_obj_func, total_size: int,
                         chunk_size: int):
    collection = mongo_db.get_collection(collection_name)
    inserted = 0
    while inserted < total_size:
        collection.insert_many(generate_objects(chunk_size, gen_obj_func))
        inserted += chunk_size


def get_mongo_objects(collection_name: str, query: dict):
    collection = mongo_db.get_collection(collection_name)
    objects = list(collection.find(query))
    return objects


def research_inserts_mongo(total_records_per_table, chunk_size):
    for coll_name, gener_func in gen_funcs.items():
        insert_mongo_objects(coll_name, gener_func, total_records_per_table,
                             chunk_size)


def clear_mongo():
    for coll_name in gen_funcs.keys():
        mongo_db.get_collection(coll_name).drop()


def fill_mongo():
    clear_mongo()
    research_inserts_mongo(INIT_RECORDS_ALL, INIT_RECORDS_CHUNK)


if __name__ == "__main__":
    try:
        start_time = time.perf_counter()
        clear_mongo()
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Took {total_time:.4f} seconds')
    except Exception as ex:
        print(f'Error {ex}')
