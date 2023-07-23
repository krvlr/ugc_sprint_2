
import time
from functools import wraps
from uuid import uuid4
from pydantic import Field
from pydantic import BaseSettings

REPEAT_TEST_COUNT = 5

USERS_COUNT = 100000
MOVIES_COUNT = 1000

INIT_RECORDS_ALL = 1000000

INIT_RECORDS_CHUNK = 10000

COUNT_OF_SELECTS = 1000

COUNT_OF_INSERTS = 15

user_ids = [str(uuid4()) for _ in range(USERS_COUNT)]
movie_ids = [str(uuid4()) for _ in range(MOVIES_COUNT)]


CHUNKS = [
    100,
    200,
    500,
    1000,
    2000,
    4000,
    5000,
    6000,
    8000,
    10_000,
    100_000,
    200_000,
    500_000,
    1_000_000,
]

SELECTING_RESULT_FILE_NAME = "selecting_results.csv"
INSERTING_RESULT_FILE_NAME = "inserting_results.csv"


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


class PerformanceSettings(BaseSettings):
    """Общие настройки"""
    dbname: str = Field(default='postgres', env='POSTGRES_NAME')
    username: str = Field(default='postgres', env='POSTGRES_USER')
    password: str = Field(default='postgres', env='POSTGRES_PASSWORD')
    host: str = Field(default='localhost', env='POSTGRES_HOST')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


perf_settings = PerformanceSettings()
