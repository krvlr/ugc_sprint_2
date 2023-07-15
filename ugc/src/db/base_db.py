import abc
from abc import ABCMeta

from pydantic import BaseModel


class QueueProvider(metaclass=ABCMeta):
    @abc.abstractmethod
    async def send(self, topic, event, key):
        pass
