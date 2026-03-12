from fastapi import APIRouter, Depends, status
from typing import List
from app.core.security import get_current_user
from app.schemas.quote import QuoteResponse, BookmarkCreate
from app.services import quote_service

router = APIRouter(prefix="/quotes", tags=["Quote"])

# 랜덤 명언 조회
@router.get("/random", response_model=QuoteResponse)
async def get_random_quote(
    current_user=Depends(get_current_user)):

    return await quote_service.get_random_quote_service()


# 내 북마크 목록 조회
@router.get("/bookmarks", response_model=List[QuoteResponse])
async def list_my_bookmarks(
    current_user=Depends(get_current_user)):

    return await quote_service.get_my_bookmarks_service(current_user.id)


# 북마크 추가
@router.post("/bookmarks", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    data: BookmarkCreate,
    current_user=Depends(get_current_user)):
    return await quote_service.add_bookmark_service(current_user.id, data.quote_id)


# 북마크 해제
@router.delete("/bookmarks/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    quote_id: int,
    current_user=Depends(get_current_user)):

    await quote_service.remove_bookmark_service(current_user.id, quote_id)