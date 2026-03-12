from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.quote import QuoteBase, BookmarkCreateRequest, BookmarkResponse
from app.services.quote_service import quote_service
from app.core.security import get_current_user

router = APIRouter()

# 1. 오늘의 랜덤 명언 조회
@router.get("/random", response_model=QuoteBase)
async def get_today_quote():

    return await quote_service.get_random_quote()

# 2. 명언 북마크 추가
@router.post("/bookmark", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite_quote(
    request: BookmarkCreateRequest,
    current_user = Depends(get_current_user) # 로그인한 유저 정보
 ):

    return await quote_service.add_bookmark(current_user.id, request.quote_id)

# 3. 내 북마크 목록 조회
@router.get("/bookmarks", response_model=List[QuoteBase])
async def get_my_quotes(current_user = Depends(get_current_user)):

    return await quote_service.get_my_bookmarks(current_user.id)

# 4. 북마크 해제 (삭제)
@router.delete("/bookmark/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite_quote(
    quote_id: int,
    current_user = Depends(get_current_user)):

    await quote_service.remove_bookmark(current_user.id, quote_id)
    return None