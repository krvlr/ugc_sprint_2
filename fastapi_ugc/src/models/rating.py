from datetime import datetime

from pydantic import BaseModel


class RatingModel(BaseModel):
    user_id: str
    film_id: str
    rating_score: int
    created: datetime


class CreateRatingModel(BaseModel):
    film_id: str
    rating_score: int


class AvgRating(BaseModel):
    film_id: str
    avg_rating_score: float


class CountRating(BaseModel):
    film_id: str
    count_rating_score: int

#
# @dataclass
# class FilmFilters:
#     genres_id: list[str] | None = Query(default=None)