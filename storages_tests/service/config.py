from random import randint, choice
from uuid import uuid4

REPEAT_TEST_COUNT = 5

USERS_COUNT = 1000000
MOVIES_COUNT = 10000

INIT_RECORDS_ALL = 10000000

INIT_RECORDS_CHUNK = 10000

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

DATA_SELECTING_RESULT_FILE_NAME = "data_selecting_results.csv"
DATA_INSERTING_RESULT_FILE_NAME = "data_inserting_results.csv"


def generate_views(num: int) -> list[tuple[str, str, int], None, None]:
    return [(choice(user_ids), choice(movie_ids), randint(10_000, 30_000)) for _ in range(num)]
