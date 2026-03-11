from fastapi import APIRouter, Depends, status
from core.security import get_current_user
from schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse, DiaryListResponse
from services.diary_service import (
    create_diary as create_diary_service,
    get_diary as get_diary_service,
    get_diary_list as get_diary_list_service,
    update_diary as update_diary_service,
    delete_diary as delete_diary_service)


router = APIRouter(prefix="/diaries", tags=["Diary"])

# 목록 조회
@router.get("", response_model=DiaryListResponse)
async def list_diaries(
        search: str = "",
        sort: str = "newest",
        page: int = 1,
        size: int = 5,
        current_user = Depends(get_current_user)
):
    return await get_diary_list_service(current_user.id, search, sort, page, size)

# 단일 조회
async def get_diary(
        diary_id: int,
        current_user = Depends(get_current_user)
):
    return await get_diary_service(diary_id, current_user.id)


# 생성
@router.post("", response_model=DiaryCreate, status_code=status.HTTP_201_CREATED)
async def create_diary(
        data: DiaryCreate,
        current_user = Depends(get_current_user)
):
    return await create_diary_service(current_user.id, data)


# 수정
@router.patch("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
        diary_id: int,
        data: DiaryUpdate,
        current_user = Depends(get_current_user)
):
    return await update_diary_service(diary_id, current_user.id, data)


# 삭제
@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
        diary_id: int,
        current_user = Depends(get_current_user)
):
    await delete_diary_service(diary_id, current_user.id)