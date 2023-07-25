from fastapi import APIRouter, Depends

from models.common import Paginator
from models.review import ReviewModel, CreateReviewModel, UpdateReviewModel
from services.auth import JWTBearer
from services.review_service import ReviewService, get_review_service

router = APIRouter()


@router.get("/", response_model=list[ReviewModel])
async def review_list(
    film_id: str = "",
    user_id: str = Depends(JWTBearer()),
    paginator: Paginator = Depends(Paginator),
    reviews_service: ReviewService = Depends(get_review_service),
) -> list[ReviewModel]:
    return await reviews_service.get_list(film_id, user_id, paginator.offset, paginator.limit)


@router.post("/create", response_model=ReviewModel)
async def review_create(
    create_review_request: CreateReviewModel,
    user_id=Depends(JWTBearer()),
    reviews_service: ReviewService = Depends(get_review_service),
) -> ReviewModel:
    return await reviews_service.create(
        user_id,
        create_review_request.film_id,
        create_review_request.text,
    )


@router.post("/update", response_model=ReviewModel)
async def review_update(
    update_review_request: UpdateReviewModel,
    user_id=Depends(JWTBearer()),
    reviews_service: ReviewService = Depends(get_review_service),
) -> ReviewModel:
    return await reviews_service.update(
        user_id,
        update_review_request.film_id,
        update_review_request.text,
    )


@router.get("/delete")
async def review_delete(
    film_id: str,
    user_id=Depends(JWTBearer()),
    reviews_service: ReviewService = Depends(get_review_service),
) -> None:
    await reviews_service.delete(user_id=user_id, film_id=film_id)
