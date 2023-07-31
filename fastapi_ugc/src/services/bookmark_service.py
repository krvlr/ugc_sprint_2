import logging
from datetime import datetime
from functools import lru_cache

from core.config import mongodb_settings
from db.base_db import DbAdapter
from db.mongodb_adapter import get_mongodb_adapter
from fastapi import Depends
from models.bookmark import BookmarkModel

from services.base_service import BaseService

logger = logging.getLogger(__name__)


class BookmarkService(BaseService):
    def __init__(self, db_adapter: DbAdapter):
        super().__init__(db_adapter=db_adapter, collection=mongodb_settings.collection_bookmark)

    async def get_list(
        self,
        user_id: str,
        offset: int,
        limit: int,
    ) -> list[BookmarkModel]:
        bookmark_list = await self.db_adapter.find(
            self.collection,
            {"user_id": user_id},
            limit=limit,
            offset=offset,
        )
        return [BookmarkModel(**bookmark) for bookmark in bookmark_list]

    async def create(
        self,
        user_id: str,
        film_id: str,
    ) -> BookmarkModel:
        bookmark = await self.db_adapter.find_one(
            self.collection, {"user_id": user_id, "film_id": film_id}
        )
        if bookmark:
            logger.info(f"Закладка уже существует для user_id: {user_id}, film_id: {film_id}")
            return BookmarkModel(**bookmark)

        bookmark = BookmarkModel(user_id=user_id, film_id=film_id, created=datetime.now())
        await self.db_adapter.insert(self.collection, bookmark.model_dump())
        return bookmark


@lru_cache()
def get_bookmark_service(db_adapter=Depends(get_mongodb_adapter)) -> BookmarkService:
    return BookmarkService(db_adapter)
