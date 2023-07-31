import logging
from datetime import datetime
from functools import lru_cache

from core.config import mongodb_settings
from db.base_db import DbAdapter
from db.mongodb_adapter import get_mongodb_adapter
from fastapi import Depends
from models.rating import RatingModel, AvgRating, CountRating

from services.base_service import BaseService

logger = logging.getLogger(__name__)


class RatingService(BaseService):
    def __init__(self, db_adapter: DbAdapter):
        super().__init__(db_adapter=db_adapter, collection=mongodb_settings.collection_rating)

    async def get_list(
        self,
        user_id: str,
        offset: int,
        limit: int,
    ) -> list[RatingModel]:
        rating_list = await self.db_adapter.find(
            self.collection,
            {"user_id": user_id},
            limit=limit,
            offset=offset,
        )
        return [RatingModel(**rating) for rating in rating_list]

    async def create(self, user_id: str, film_id: str, rating_score: int) -> RatingModel:
        rating = await self.db_adapter.find_one(
            self.collection, {"user_id": user_id, "film_id": film_id}
        )
        if rating:
            logger.info(f"Рейтинг уже выставлен для user_id: {user_id}, film_id: {film_id}")
            return RatingModel(**rating)

        rating = RatingModel(
            user_id=user_id, film_id=film_id, rating_score=rating_score, created=datetime.now()
        )
        await self.db_adapter.insert(self.collection, rating.model_dump())
        return rating

    async def update(self, user_id: str, film_id: str, rating_score: int) -> RatingModel:
        rating = RatingModel(
            user_id=user_id, film_id=film_id, rating_score=rating_score, created=datetime.now()
        )
        await self.db_adapter.update(
            self.collection,
            {"user_id": user_id, "film_id": film_id},
            rating.model_dump(),
        )
        return rating

    async def get_count_of_ratings(self, film_id: str) -> CountRating:
        rating_count = await self.db_adapter.count(self.collection, {"film_id": film_id})
        return CountRating(film_id=film_id, count_rating_score=rating_count)

    async def get_avg_ratings_of_film(self, film_id: str) -> AvgRating:
        pipeline = [
            {"$match": {"film_id": film_id}},
            {"$group": {"_id": "@film_id", "avg_score": {"$avg": "$rating_score"}}},
        ]
        avg_rating = await self.db_adapter.avg(self.collection, pipeline)
        return AvgRating(film_id=film_id, avg_rating_score=avg_rating)


@lru_cache()
def get_rating_service(
    db_adapter=Depends(get_mongodb_adapter),
) -> RatingService:
    return RatingService(db_adapter)
