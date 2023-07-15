from pydantic import BaseModel


class FilmProgress(BaseModel):
    user_id: str
    movie_id: str
    timestamp_of_film: str
