import abc
from abc import ABCMeta


class DbAdapter(metaclass=ABCMeta):
    @abc.abstractmethod
    async def find(self, collection: str, filters: dict, limit: int, offset: int) -> list[dict]:
        pass

    @abc.abstractmethod
    async def find_one(self, collection: str, filters: dict) -> dict | None:
        pass

    @abc.abstractmethod
    async def insert(self, collection: str, data: dict) -> None:
        pass

    @abc.abstractmethod
    async def update(self, collection: str, filters: dict, data: dict) -> None:
        pass

    @abc.abstractmethod
    async def delete(self, collection: str, filters: dict) -> None:
        pass

    @abc.abstractmethod
    async def count(self, collection: str, filters: dict) -> int | None:
        pass

    @abc.abstractmethod
    async def avg(self, collection: str, pipeline: list | dict) -> float | None:
        pass
