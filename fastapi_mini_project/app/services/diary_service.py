from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.diary_repo import diary_repository
from schemas.diary import DiaryCreate, DiaryUpdate


class DiaryService:
    def create_diary(self, db: Session, user_id: int, data: DiaryCreate):
        return diary_repository.create(db, user_id, data)


    def update_diary(self, db: Session, diary_id: int, user_id: int, data: DiaryUpdate):
        diary = self.get_diary(db, diary_id, user_id)
        return diary_repository.update(db, diary, data)


    def delete_diary(self, db: Session, diary_id: int, user_id: int):
        diary = self.get_diary(db, diary_id, user_id)
        diary_repository.delete(db, diary)


diary_service = DiaryService()