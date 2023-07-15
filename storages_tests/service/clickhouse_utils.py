from time import time

from clickhouse_driver import Client

client = Client(host="localhost")


def select_ids(field):
    return [str(_id[0]) for _id in client.execute(f"SELECT DISTINCT {field} from research.views")]


def time_execute(query: str, values: list | dict) -> float:
    start = time()
    client.execute(query, values)
    return round(time() - start, 4)
