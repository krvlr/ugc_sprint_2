from fastapi import APIRouter, Depends

from models.bookmark import BookmarkModel, CreateBookmarkModel
from models.common import Paginator
from services.auth import JWTBearer
from services.bookmark_service import BookmarkService, get_bookmark_service

router = APIRouter()


@router.get("/", response_model=list[BookmarkModel])
async def bookmark_list(
    user_id: str = Depends(JWTBearer()),
    paginator: Paginator = Depends(Paginator),
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> list[BookmarkModel]:
    return await bookmark_service.get_list(user_id, paginator.offset, paginator.limit)


@router.post("/create", response_model=BookmarkModel)
async def bookmark_create(
    create_bookmark_request: CreateBookmarkModel,
    user_id: str = Depends(JWTBearer()),
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> BookmarkModel:
    return await bookmark_service.create(user_id, create_bookmark_request.film_id)


@router.get("/delete")
async def bookmark_delete(
    film_id: str,
    user_id: str = Depends(JWTBearer()),
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
) -> None:
    await bookmark_service.delete(user_id, film_id)
