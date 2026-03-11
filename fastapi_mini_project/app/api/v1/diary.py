from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from schemas.diary import DiaryCreate, DiaryUpdate
from services.diary_service import diary_service

router = APIRouter(prefix="/diaries", tags=["Diary"])


@router.post("", response_model=DiaryCreate, status_code=status.HTTP_201_CREATED)
def create_diary(
        data: DiaryCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return diary_service.create_diary(db, current_user.id, data)


@router.patch("/{diary_id}", response_model=DiaryResponse)
def update_diary(
        diary_id: int,
        data: DiaryUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return diary_service.update_diary(db, diary_id, current_user.id, data)


@router.delete("/{diary_id}")

