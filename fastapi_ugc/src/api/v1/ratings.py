from fastapi import APIRouter, Depends

from models.common import Paginator
from models.rating import RatingModel, CreateRatingModel, AvgRating, CountRating
from services.auth import JWTBearer
from services.rating_service import RatingService, get_rating_service

router = APIRouter()


@router.get("/", response_model=list[RatingModel])
async def rating_list(
    user_id: str = Depends(JWTBearer()),
    paginator: Paginator = Depends(Paginator),
    rating_service: RatingService = Depends(get_rating_service),
) -> list[RatingModel]:
    return await rating_service.get_list(user_id, paginator.offset, paginator.limit)


@router.post("/create", response_model=RatingModel)
async def rating_create(
    create_rating_request: CreateRatingModel,
    user_id: str = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
) -> RatingModel:
    return await rating_service.create(
        user_id, create_rating_request.film_id, create_rating_request.rating_score
    )


@router.delete("/delete")
async def rating_delete(
    film_id: str,
    user_id: str = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
) -> None:
    await rating_service.delete(user_id, film_id)


@router.put("/update", response_model=RatingModel)
async def rating_update(
    update_rating: CreateRatingModel,
    user_id: str = Depends(JWTBearer()),
    rating_service: RatingService = Depends(get_rating_service),
) -> RatingModel:
    return await rating_service.update(user_id, update_rating.film_id, update_rating.rating_score)


@router.get("/avg/{film_id}", response_model=AvgRating)
async def avg_rating(
    film_id: str,
    rating_service: RatingService = Depends(get_rating_service),
) -> AvgRating:
    return await rating_service.get_avg_ratings_of_film(film_id)


@router.get("/count/{film_id}", response_model=CountRating)
async def count_rating(
    film_id: str,
    rating_service: RatingService = Depends(get_rating_service),
) -> CountRating:
    return await rating_service.get_count_of_ratings(film_id)
