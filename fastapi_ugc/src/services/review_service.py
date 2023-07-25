import logging
from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException

from core.config import mongodb_settings
from db.base_db import DbAdapter
from db.mongodb_adapter import get_mongodb_adapter
from models.review import ReviewModel

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, db_adapter: DbAdapter):
        self.db_adapter = db_adapter

    async def get_list(self, film_id: str, user_id: str, offset: int, limit: int) -> list[ReviewModel]:
        if film_id:
            review_list = await self.db_adapter.find(
                mongodb_settings.collection_review, {"film_id": film_id}, limit, offset
            )
        else:
            review_list = await self.db_adapter.find(
                mongodb_settings.collection_review, {"user_id": user_id}, limit, offset
            )
        return [ReviewModel(**review) for review in review_list]

    async def create(self, user_id: str, film_id: str, text: str) -> ReviewModel:
        review = await self.db_adapter.find_one(
            mongodb_settings.collection_review, {"user_id": user_id, "film_id": film_id}
        )
        if review:
            logger.info(f"Закладка уже существует для user_id: {user_id}, film_id: {film_id}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        review = ReviewModel(user_id=user_id, film_id=film_id, text=text, created=datetime.now())
        await self.db_adapter.insert(mongodb_settings.collection_review, review.model_dump())
        return review

    async def update(self, user_id: str, film_id: str, text: str) -> ReviewModel:
        review = ReviewModel(user_id=user_id, film_id=film_id, text=text, created=datetime.now())
        await self.db_adapter.update(
            mongodb_settings.collection_review,
            {"user_id": user_id, "film_id": film_id},
            review.model_dump(),
        )
        return review

    async def delete(self, user_id: str, film_id: str) -> None:
        review = await self.db_adapter.find_one(
            mongodb_settings.collection_review, {"user_id": user_id, "film_id": film_id}
        )

        if not review:
            logger.info(f"Отзыва не существует для user_id: {user_id}, film_id: {film_id}")
            return

        await self.db_adapter.delete(mongodb_settings.collection_review, {"user_id": user_id, "film_id": film_id})


@lru_cache()
def get_review_service(db_adapter=Depends(get_mongodb_adapter)) -> ReviewService:
    return ReviewService(db_adapter)
