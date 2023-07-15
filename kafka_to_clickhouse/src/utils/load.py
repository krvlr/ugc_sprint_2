import abc
from abc import ABCMeta
from clickhouse_driver import Client
from utils.utils import backoff


class Loader(metaclass=ABCMeta):
    @abc.abstractmethod
    def init_db(self):
        pass

    @abc.abstractmethod
    def save_data(self, events):
        pass


class ClickHouseLoader(Loader):
    """
    Класс для загрузки данных в подготовленном формате в ClickHouse.
    """

    def __init__(self, client: Client):
        self.client = client
        self.init_db()

    @backoff()
    def init_db(self):
        self.client.execute(
            "CREATE DATABASE IF NOT EXISTS movies_events ON CLUSTER company_cluster"
        )
        self.client.execute(
            """
            CREATE TABLE IF NOT EXISTS movies_events.regular_table ON CLUSTER company_cluster
            (user_id String, movie_id String, timestamp_of_film String)
            Engine=MergeTree()
            ORDER BY user_id
            """
        )

    @backoff()
    def save_data(self, events):
        """Метод для вставки событий в СlickHouse батчами."""
        self.client.execute(
            """
            INSERT INTO movies_events.regular_table (user_id, movie_id, timestamp_of_film)
            VALUES
            """,
            events,
        )
