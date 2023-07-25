import logging
from datetime import datetime
from functools import lru_cache

from fastapi import Depends

from core.config import mongodb_settings
from db.base_db import DbAdapter
from db.mongodb_adapter import get_mongodb_adapter
from models.bookmark import BookmarkModel

logger = logging.getLogger(__name__)


class BookmarkService:
    def __init__(self, db_adapter: DbAdapter):
        self.db_adapter = db_adapter

    async def get_list(
        self,
        user_id: str,
        offset: int,
        limit: int,
    ) -> list[BookmarkModel]:
        bookmark_list = await self.db_adapter.find(
            mongodb_settings.collection_bookmark,
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
            mongodb_settings.collection_bookmark, {"user_id": user_id, "film_id": film_id}
        )
        if bookmark:
            logger.info(f"Закладка уже существует для user_id: {user_id}, film_id: {film_id}")
            return BookmarkModel(**bookmark)
        else:
            bookmark = BookmarkModel(user_id=user_id, film_id=film_id, created=datetime.now())
            await self.db_adapter.insert(
                mongodb_settings.collection_bookmark, bookmark.model_dump()
            )
            return bookmark

    async def delete(self, user_id, film_id) -> None:
        bookmark = await self.db_adapter.find_one(
            mongodb_settings.collection_bookmark, {"user_id": user_id, "film_id": film_id}
        )
        if not bookmark:
            logger.info(f"Закладка не существует для user_id: {user_id}, film_id: {film_id}")
            return

        await self.db_adapter.delete(
            mongodb_settings.collection_bookmark, {"user_id": user_id, "film_id": film_id}
        )


@lru_cache()
def get_bookmark_service(db_adapter=Depends(get_mongodb_adapter)) -> BookmarkService:
    return BookmarkService(db_adapter)
