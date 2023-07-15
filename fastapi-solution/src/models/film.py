from dataclasses import dataclass

from fastapi import Query
from models.shared import BaseOrjsonModel
from pydantic import BaseModel


@dataclass
class FilmFilters:
    genres_id: list[str] | None = Query(default=None)
    genres_name: list[str] | None = Query(default=None)
    actors_id: list[str] | None = Query(default=None)
    actors_name: list[str] | None = Query(default=None)
    writers_id: list[str] | None = Query(default=None)
    writers_name: list[str] | None = Query(default=None)
    directors_id: list[str] | None = Query(default=None)
    directors_name: list[str] | None = Query(default=None)


class FilmPerson(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class FilmBrief(BaseOrjsonModel):
    id: str
    title: str
    imdb_rating: float


class FilmDetail(FilmBrief):
    description: str | None
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]
    genres: list[FilmGenre]


class FilmProgress(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str
