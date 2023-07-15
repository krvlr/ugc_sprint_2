import logging
from db.kafka_provider import KafkaQueueProvider, get_kafka_queue_provider
from core.config import kafka_settings
from models.film import FilmProgress

from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)


router = APIRouter()


@router.put("/register_progress")
async def register_film_timestamp(
    film_progress: FilmProgress,
    queue_provider: KafkaQueueProvider = Depends(get_kafka_queue_provider),
):
    event = film_progress.dict()
    key = event["user_id"] + event["movie_id"]
    await queue_provider.send(topic=kafka_settings.topic, event=event, key=key)
    return {"status": "OK"}
