from fastapi import APIRouter, Depends, status
from core.security import get_current_user
from schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from services.diary_service import diary_service


router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("", response_model=DiaryCreate, status_code=status.HTTP_201_CREATED)
async def create_diary(
        data: DiaryCreate,
        current_user = Depends(get_current_user)
):
    return await diary_service.create_diary(current_user.id, data)


@router.patch("/{diary_id}", response_model=DiaryResponse)
async def update_diary(
        diary_id: int,
        data: DiaryUpdate,
        current_user = Depends(get_current_user)
):
    return await diary_service.update_diary(diary_id, current_user.id, data)


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
        diary_id: int,
        current_user = Depends(get_current_user)
):
    await diary_service.delete_diary(diary_id, current_user.id)