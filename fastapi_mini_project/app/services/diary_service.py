from fastapi import HTTPException, status
from app.repositories.diary_repo import (
    create, get_by_id, get_list, update, delete
)
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryListResponse
from typing import Optional


class DiaryService:
    # Create
    async def create_diary(self, user_id: int, data: DiaryCreate):
        return await create(user_id, data)

    # Read (단일)
    async def get_diary(self, diary_id: int, user_id: int):
        diary = await get_by_id(diary_id, user_id)
        if not diary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="일기를 찾을 수 없습니다."
            )
        return diary

    # Read (목록), size(한 번에 볼 수 있는 목록 갯수, 임의로 정할 수 있지만 20이하만 볼 수 있도록 정함)
    async def get_diary_list(
            self,
            user_id: Optional[int] = None,
            search: str = "",
            sort: str = "newest",
            page: int = 1,
            size: int = 5
    ) -> DiaryListResponse:
        if page < 1:
            raise HTTPException(status_code=400, detail="페이지는 1이상이어야 합니다.")
        if size < 5 or size > 20:
            raise HTTPException(status_code=400, detail="목록은 5이상 20이하여야 합니다.")

        total, diaries = await get_list(user_id, search, sort, page, size)

        return DiaryListResponse(
            total=total,
            page=page,
            size=size,
            diaries=diaries
        )


    # Update
    async def update_diary(self, diary_id: int, user_id: int, data: DiaryUpdate):
        diary = await self.get_diary(diary_id, user_id)
        return await update(diary, data)

    # Delete
    async def delete_diary(self, diary_id: int, user_id: int):
        diary = await self.get_diary(diary_id, user_id)
        await delete(diary)


diary_service = DiaryService()