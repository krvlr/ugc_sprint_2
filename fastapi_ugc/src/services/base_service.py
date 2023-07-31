import logging

from db.base_db import DbAdapter

logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, db_adapter: DbAdapter, collection: str):
        self.db_adapter = db_adapter
        self.collection = collection

    async def delete(self, user_id: str, film_id: str) -> None:
        row = await self.db_adapter.find_one(
            self.collection, {"user_id": user_id, "film_id": film_id}
        )
        if not row:
            logger.info(
                f"Записи в коллекции {self.collection} не существует "
                f"для user_id: {user_id}, film_id: {film_id}"
            )
            return

        await self.db_adapter.delete(self.collection, {"user_id": user_id, "film_id": film_id})
