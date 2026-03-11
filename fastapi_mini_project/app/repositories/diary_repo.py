from sqlalchemy.orm import Session
from models.diary import Diary
from schemas.diary import DiaryCreate, DiaryUpdate
from typing import Optional


class DiaryRepo:
    def create(self, db: Session, user_id: int, data: DiaryCreate) -> Diary:
        diary = Diary(
            user_id=user_id,
            title=data.title,
            content=data.content
        )

        db.add(diary)
        db.commit()
        db.refresh(diary)
        return diary


    def update(self, db: Session, diary: Diary, data: DiaryUpdate) -> Diary:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(diary, field, value)

        db.commit()
        db.refresh(diary)
        return diary


    def delete(self, db: Session, diary: Diary):
        pass