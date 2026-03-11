from models.diary import Diary
from schemas.diary import DiaryCreate, DiaryUpdate
from typing import Optional


class DiaryRepo:
    async def create(self, user_id: int, data: DiaryCreate) -> Diary:
        diary = await Diary.create(
            user_id=user_id,
            title=data.title,
            content=data.content
        )

        return diary


    async def update(self, diary: Diary, data: DiaryUpdate) -> Diary:
        update_data = data.model_dump(exclude_unset=True)
        await diary.update_from_dict(update_data).save()
        return diary


    async def delete(self, diary: Diary) -> None:
        await diary.delete()


diary_repository = DiaryRepo()