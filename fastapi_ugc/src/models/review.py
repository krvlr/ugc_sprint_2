from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class ReviewModel(BaseModel):
    user_id: str
    film_id: str
    text: str
    created: datetime


class CreateReviewModel(BaseModel):
    film_id: str
    text: str = Query(default=None, min_length=5, max_length=1000)


class UpdateReviewModel(CreateReviewModel):
    pass
