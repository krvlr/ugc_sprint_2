import datetime
import json
import logging
import random
import uuid
from time import sleep

from clickhouse_driver import Client
from confluent_kafka.cimpl import Producer
from pydantic import BaseModel
from core.settings import test_base_settings

producer = Producer(
    {"bootstrap.servers": f"{test_base_settings.kafka_host}:{test_base_settings.kafka_port}"}
)

clickhouse_client = Client(
    host=test_base_settings.clickhouse_host,
    alt_hosts="clickhouse-node2, clickhouse-node3, clickhouse-node4",
)


class FilmProgress(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str


def fill_random_kafka():
    """Заполнить Kafka тестовыми событиями"""
    count_of_events = random.randint(1, 100)
    for _ in range(count_of_events):
        f = FilmProgress(
            user_id=str(uuid.uuid4()),
            movie_id=str(uuid.uuid4()),
            timestamp_of_film=str(datetime.datetime.utcnow()),
        )
        event = f.dict()
        key = event["user_id"] + event["movie_id"]
        producer.produce(topic="movies_views", value=json.dumps(event).encode("utf-8"), key=key)
    producer.flush()
    sleep(1)
    return count_of_events


def fill_random_kafka_events():
    """Заполнить Kafka тестовыми событиями и вернуть список событий"""
    count_of_events = random.randint(1, 100)
    events = []
    for _ in range(count_of_events):
        f = FilmProgress(
            user_id=str(uuid.uuid4()),
            movie_id=str(uuid.uuid4()),
            timestamp_of_film=str(datetime.datetime.utcnow()),
        )
        event = f.dict()
        events.append(list(event.values()))
        key = event["user_id"] + event["movie_id"]
        producer.produce(topic="movies_views", value=json.dumps(event).encode("utf-8"), key=key)
    producer.flush()
    sleep(1)
    return events


def get_events_from_clickhouse():
    events = clickhouse_client.execute(
        """
        SELECT * FROM movies_events.regular_table
        """
    )
    return events


def clear_clickhouse():
    clickhouse_client.execute(
        """
        TRUNCATE TABLE IF EXISTS movies_events.regular_table
        """
    )


def test_kafka_to_clickhouse_count():
    """Тест на проверку количества событий в кафке и после etl в clickhouse"""
    clear_clickhouse()
    count_of_events = fill_random_kafka()
    events_size = 0
    count_of_attempts = 0
    while events_size != count_of_events and count_of_attempts < 5:
        events = get_events_from_clickhouse()
        events_size = len(events)
        count_of_attempts += 1
        sleep(3)
    assert events_size == count_of_events
    assert count_of_attempts < 5


def test_compare_events():
    """Тест на проверку, что все данные в событиях kafka и clickhouse совпадают"""
    clear_clickhouse()
    events_kafka = fill_random_kafka_events()
    events_size = 0
    count_of_attempts = 0
    while events_size != len(events_kafka) and count_of_attempts < 5:
        events = get_events_from_clickhouse()
        events_size = len(events)
        count_of_attempts += 1
        sleep(3)
    events_kafka.sort()
    if events_size == len(events_kafka):
        for i in range(len(events)):
            for field in range(3):
                assert events[i][field] == events_kafka[i][field]

    assert events_size == len(events_kafka)
    assert count_of_attempts < 5
