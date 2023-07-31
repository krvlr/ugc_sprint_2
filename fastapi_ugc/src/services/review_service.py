import logging
from datetime import datetime
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException

from core.config import mongodb_settings
from db.base_db import DbAdapter
from db.mongodb_adapter import get_mongodb_adapter
from models.review import ReviewModel

from services.base_service import BaseService

logger = logging.getLogger(__name__)


class ReviewService(BaseService):
    def __init__(self, db_adapter: DbAdapter):
        super().__init__(db_adapter=db_adapter, collection=mongodb_settings.collection_review)

    async def get_list(
        self, film_id: str, user_id: str, offset: int, limit: int
    ) -> list[ReviewModel]:
        if film_id:
            review_list = await self.db_adapter.find(
                self.collection, {"film_id": film_id}, limit, offset
            )
        else:
            review_list = await self.db_adapter.find(
                self.collection, {"user_id": user_id}, limit, offset
            )
        return [ReviewModel(**review) for review in review_list]

    async def create(self, user_id: str, film_id: str, text: str) -> ReviewModel:
        review = await self.db_adapter.find_one(
            self.collection, {"user_id": user_id, "film_id": film_id}
        )
        if review:
            logger.info(f"Закладка уже существует для user_id: {user_id}, film_id: {film_id}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        review = ReviewModel(user_id=user_id, film_id=film_id, text=text, created=datetime.now())
        await self.db_adapter.insert(self.collection, review.model_dump())
        return review

    async def update(self, user_id: str, film_id: str, text: str) -> ReviewModel:
        review = ReviewModel(user_id=user_id, film_id=film_id, text=text, created=datetime.now())
        await self.db_adapter.update(
            self.collection,
            {"user_id": user_id, "film_id": film_id},
            review.model_dump(),
        )
        return review


@lru_cache()
def get_review_service(db_adapter=Depends(get_mongodb_adapter)) -> ReviewService:
    return ReviewService(db_adapter)
