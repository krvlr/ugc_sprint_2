from typing import Optional

from db.base_db import QueueProvider

from aiokafka import AIOKafkaProducer
import json


kafka_producer: Optional[AIOKafkaProducer] = None


class KafkaQueueProvider(QueueProvider):
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self.kafka_producer = kafka_producer

    async def send(self, topic, event, key):
        await self.kafka_producer.send_and_wait(
            topic=topic, value=json.dumps(event).encode("utf-8"), key=key.encode("utf-8")
        )


async def get_kafka_queue_provider() -> AIOKafkaProducer:
    return KafkaQueueProvider(kafka_producer=kafka_producer)
