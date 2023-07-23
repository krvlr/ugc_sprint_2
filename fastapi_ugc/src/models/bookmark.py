from datetime import datetime

from pydantic import BaseModel


class BookmarkModel(BaseModel):
    user_id: str
    film_id: str
    created: datetime


class CreateBookmarkModel(BaseModel):
    film_id: str
