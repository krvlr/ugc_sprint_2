from typing import Type

from pydantic import BaseModel

from decorators import backoff


class DataTransform:
    @backoff()
    def validate_and_transform(
        self, model: Type[BaseModel], objects: list[dict]
    ) -> list[BaseModel]:
        return [model(**dict(obj)) for obj in objects]
