from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import mongodb_settings
from db.base_db import DbAdapter

client: AsyncIOMotorClient = None


def get_mongodb_client() -> AsyncIOMotorClient:
    return client


class MongodbAdapter(DbAdapter):
    def __init__(self, data_provider: AsyncIOMotorClient):
        self.data_provider = data_provider
        self.db = self.data_provider[mongodb_settings.db_name]

    async def find(self, collection: str, filters: dict, limit: int, offset: int) -> list[dict]:
        return [row async for row in self.db[collection].find(filters).skip(offset).limit(limit)]

    async def find_one(self, collection: str, filters: dict) -> dict | None:
        return await self.db[collection].find_one(filters)

    async def insert(self, collection: str, data: dict) -> None:
        await self.db[collection].insert_one(data)

    async def delete(self, collection: str, filters: dict) -> None:
        await self.db[collection].find_one_and_delete(filters)


def get_mongodb_adapter(
    data_provider=Depends(get_mongodb_client),
) -> MongodbAdapter:
    return MongodbAdapter(data_provider)
