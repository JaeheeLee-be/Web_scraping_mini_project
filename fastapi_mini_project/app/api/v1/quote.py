from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.quote import QuoteResponse, BookmarkCreate
from app.services import quote_service
from app.api.v1.auth import get_current_user  # 인증 관련 의존성 (팀원 작업 확인 필요)

router = APIRouter()

# 1. 랜덤 명언 조회
@router.get("/random", response_model=QuoteResponse)
async def get_random_quote():
    """
    등록된 명언 중 하나를 랜덤으로 반환합니다.
    """
    return await quote_service.get_random_quote_service()


# 2. 내 북마크 목록 조회
@router.get("/bookmarks", response_model=List[QuoteResponse])
async def get_my_bookmarks(current_user=Depends(get_current_user)):
    """
    로그인한 사용자가 북마크한 모든 명언을 조회합니다.
    """
    return await quote_service.get_my_bookmarks_service(user_id=current_user.id)


# 3. 명언 북마크 추가
@router.post("/bookmarks", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    bookmark_data: BookmarkCreate,
    current_user=Depends(get_current_user)
):
    """
    특정 명언을 내 북마크에 추가합니다. (중복 방지 포함)
    """
    return await quote_service.add_bookmark_service(
        user_id=current_user.id,
        quote_id=bookmark_data.quote_id
    )


# 4. 북마크 해제
@router.delete("/bookmarks/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_bookmark(
    quote_id: int,
    current_user=Depends(get_current_user)
):
    """
    북마크를 해제합니다.
    """
    await quote_service.remove_bookmark_service(
        user_id=current_user.id,
        quote_id=quote_id
    )
    return None