from fastapi import HTTPException, status
from repositories.diary_repo import diary_repository
from schemas.diary import DiaryCreate, DiaryUpdate


class DiaryService:
    async def create_diary(self, user_id: int, data: DiaryCreate):
        return await diary_repository.create(user_id, data)


    async def update_diary(self, diary_id: int, user_id: int, data: DiaryUpdate):
        diary = await self.get_diary(diary_id, user_id)
        return await diary_repository.update(diary, data)


    async def delete_diary(self, diary_id: int, user_id: int):
        diary = await self.get_diary(diary_id, user_id)
        await diary_repository.delete(diary)


diary_service = DiaryService()