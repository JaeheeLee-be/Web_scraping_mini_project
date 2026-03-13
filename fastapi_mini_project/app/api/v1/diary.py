from fastapi import APIRouter, Depends, status
from app.core.security import get_current_user
from app.schemas.diary import (
    DiaryCreate,
    DiaryUpdate,
    DiaryResponse,
    DiaryListResponse,
)
from app.services.diary_service import diary_service
from app.schemas.quote import QuoteResponse

router = APIRouter(prefix="/diaries", tags=["Diary"])

# 1. 목록 조회
@router.get("", response_model=DiaryListResponse)
async def list_diaries(
    search: str = "",
    sort: str = "newest",
    page: int = 1,
    size: int = 5,

):
    return await diary_service.get_diary_list(search, sort, page, size)

# 2. 랜덤 명언/일기
@router.get("/random", response_model=QuoteResponse)
async def get_random_quote():
    return await diary_service.get_random_quote()

# 3. 단일 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(
    diary_id: int,
):
    return await diary_service.get_diary(diary_id)

# 4. 생성
@router.post("", response_model=DiaryResponse, status_code=status.HTTP_201_CREATED)
async def create_diary(
    data: DiaryCreate,
    current_user = Depends(get_current_user)
):
    return await diary_service.create_diary(current_user.id, data)

# 5. 수정
@router.patch("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
    diary_id: int,
    data: DiaryUpdate,
    current_user = Depends(get_current_user)
):
    return await diary_service.update_diary(diary_id, current_user.id, data)

# 6. 삭제
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user = Depends(get_current_user)
):
    await diary_service.delete_diary(diary_id, current_user.id)
    return None