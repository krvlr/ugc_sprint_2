import logging
from dataclasses import asdict
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import FilmBrief, FilmDetail, FilmFilters, FilmProgress
from models.shared import Paginator
from services.auth import JWTBearerPremium
from services.films import FilmService, get_film_service

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/search", response_model=list[FilmBrief])
async def film_search(
    query: str | None = None,
    sort: list[str] | None = Query(default=None),
    filters: FilmFilters = Depends(FilmFilters),
    paginator: Paginator = Depends(Paginator),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBrief]:
    return await film_service.get_by_query(
        query, sort, paginator.page_number, paginator.page_size, asdict(filters)
    )


@router.get("/", response_model=list[FilmBrief])
async def film_list(
    sort: list[str] | None = Query(default=None),
    filters: FilmFilters = Depends(FilmFilters),
    paginator: Paginator = Depends(Paginator),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBrief]:
    return await film_service.get_list(
        sort, paginator.page_number, paginator.page_size, asdict(filters)
    )


@router.get("/{film_id}", dependencies=[Depends(JWTBearerPremium())], response_model=FilmDetail)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_by_id(film_id, model_cls=FilmDetail)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film
