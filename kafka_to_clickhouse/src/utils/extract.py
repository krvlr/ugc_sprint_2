import json
import logging

import abc
from abc import ABCMeta
from confluent_kafka.cimpl import Consumer
from utils.utils import backoff

logger = logging.getLogger(__name__)


class Extractor(metaclass=ABCMeta):
    @abc.abstractmethod
    def get_batch_extractor(self, batch_size: int, timeout: int):
        pass


class KafkaExtractor(Extractor):
    """Класс для выгрузки данных из топиков Kafka."""

    def __init__(self, consumer: Consumer, topics=list[str]):
        self.consumer = consumer
        self.consumer.subscribe(topics=topics)

    @backoff()
    def get_batch_extractor(self, batch_size: int = 100, timeout: int = 5):
        """Метод для вычитывания событий из Kafka."""
        events = self.consumer.consume(num_messages=batch_size, timeout=timeout)
        logger.info(f"Extract {len(events)} evens")

        for event in events:
            yield json.loads(event.value().decode("utf-8"))
