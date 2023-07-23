import datetime
import random
from time import time

from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Iterable, Any

from db_research.service.config import (INIT_RECORDS_ALL, INIT_RECORDS_CHUNK,
                                        COUNT_OF_SELECTS)
from db_research.service.config import user_ids, movie_ids

mongo_cl: MongoClient = MongoClient('mongodb://root:example@localhost:27017/')
mongo_db = mongo_cl.get_database('events')

likes_collection = mongo_db.get_collection('likes')
reviews_collection = mongo_db.get_collection('reviews')
bookmarks_collection = mongo_db.get_collection('bookmarks')


def generate_like(movie_id: str | None = None) -> dict:
    return {
        "user_id": random.choice(user_ids),
        "movie_id": movie_id if movie_id else random.choice(movie_ids),
        "like_score": random.randint(0, 10),
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    }


def generate_review() -> dict:
    user = random.choice(user_ids)
    movie = random.choice(movie_ids)
    return {
        'user_id': user,
        'movie_id': movie,
        'review': f'Review of {movie} from {user} ',
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    }


def generate_bookmark() -> dict:
    user = random.choice(user_ids)
    movie = random.choice(movie_ids)
    return {
        'user_id': user,
        'movie_id': movie,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    }


gen_funcs = {'likes': generate_like,
             'reviews': generate_review,
             'bookmarks': generate_bookmark}


def generate_objects(chunk_size: int, gen_func) -> list:
    return [(gen_func()) for _ in range(chunk_size)]


def insert_mongo_gen_objects(collection_name: str, gen_obj_func, total_size: int, chunk_size: int):
    collection = mongo_db.get_collection(collection_name)
    inserted = 0
    while inserted < total_size:
        collection.insert_many(generate_objects(chunk_size, gen_obj_func))
        inserted += chunk_size


def get_mongo_objects(collection_name: str, query: dict):
    collection = mongo_db.get_collection(collection_name)
    objects = list(collection.find(query))
    return objects


def clear_mongo():
    for coll_name in gen_funcs.keys():
        mongo_db.get_collection(coll_name).drop()


def fill_mongo():
    print('Started filling mongo')
    start = time()
    clear_mongo()
    for coll_name, gener_func in gen_funcs.items():
        insert_mongo_gen_objects(coll_name, gener_func, INIT_RECORDS_ALL,
                                 INIT_RECORDS_CHUNK)
    print('Filling mongo time ', round(time() - start, 4))


def time_execute_mongo(collection,
                       query: list | dict | None = None,
                       values: list | dict | None | Iterable[Any] = None,
                       type_f='Find') -> float:
    start = time()
    if type_f == 'Insert':
        collection.insert_many(values)
    elif type_f == 'Find':
        collection.find(query)
    elif type_f == 'Count':
        collection.count_documents(query)
    elif type_f == 'Aggr':
        collection.aggregate(query)
    return round(time() - start, 8)


def time_get_likes_user():
    query_mongo = {'user_id': random.choice(user_ids)}
    sum_time = sum((time_execute_mongo(likes_collection, query_mongo, type_f='Find')) for _ in
                   range(COUNT_OF_SELECTS))
    print('mongo likes of user time', sum_time)
    return sum_time


def time_count_likes_movie():
    query_mongo = {'movie_id': random.choice(movie_ids)}
    sum_time = time_execute_mongo(likes_collection, query_mongo, type_f='Count')
    print('mongo count likes of movie time', sum_time)
    return sum_time


def time_get_bookmarks_user():
    query_mongo = {'user_id': random.choice(user_ids)}
    sum_time = sum((time_execute_mongo(bookmarks_collection, query_mongo, type_f='Find')) for _ in
                   range(COUNT_OF_SELECTS))
    print('mongo bookmarks of user', sum_time)
    return sum_time


def time_avg_score():
    pipeline = [
        {"$match": {"movie_id": random.choice(movie_ids)}},
        {"$group": {"_id": "@movie_id", "avg_score": {"$avg": "$like_score"}}}
    ]
    sum_time = time_execute_mongo(likes_collection, pipeline, type_f='Aggr')
    print('mongo avg score time', sum_time)
    return sum_time


def time_insert_likes():
    chunk_likes = generate_objects(INIT_RECORDS_CHUNK, generate_like)
    sum_time = time_execute_mongo(likes_collection, values=chunk_likes, type_f='Insert')
    print('mongo insert likes', sum_time)
    return sum_time


def time_insert_reviews():
    chunk_reviews = generate_objects(INIT_RECORDS_CHUNK, generate_review)
    sum_time = time_execute_mongo(likes_collection, values=chunk_reviews, type_f='Insert')
    print('mongo insert review', sum_time)
    return sum_time


def time_insert_bookmarks():
    chunk_bookmarks = generate_objects(INIT_RECORDS_CHUNK, generate_bookmark)
    sum_time = time_execute_mongo(likes_collection, values=chunk_bookmarks, type_f='Insert')
    print('mongo insert bookmarks', sum_time)
    return sum_time


if __name__ == "__main__":
    try:
        fill_mongo()
    except Exception as ex:
        print(f'Error {ex}')
