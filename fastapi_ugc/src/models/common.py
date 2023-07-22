from fastapi import Query
from pydantic import BaseModel


class Paginator(BaseModel):
    offset: int = Query(default=0, ge=0)
    limit: int = Query(default=20, ge=1, le=50)
