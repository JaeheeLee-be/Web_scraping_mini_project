from app.models.diary import Diary
from app.schemas.diary import DiaryCreate, DiaryUpdate
from typing import Optional
from tortoise.expressions import Q


# Create
async def create(user_id: int, data: DiaryCreate) -> Diary:
    diary = await Diary.create(
        user_id=user_id,
        title=data.title,
        content=data.content,
    )
    return diary

# Read (단일)
async def get_by_id(diary_id: int, user_id: int) -> Optional[Diary]:
    return await Diary.filter(id=diary_id, user_id=user_id).first()

# Read (목록, 검색, 정렬, 페이징)
async def get_list(
        user_id: int,
        search: str = "",
        sort: str = "newest",
        page: int = 1,
        size: int = 5
) -> tuple[int, list[Diary]]:

    query = Diary.filter(user_id=user_id)

    # 검색
    if search:
        query = query.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    # 정렬
    order = "created_at" if sort == "oldest" else "-created_at"
    query = query.order_by(order)

    total = await query.count()
    diaries = await query.offset((page - 1) * size).limit(size)

    return total, diaries

# Update
async def update(diary: Diary, data: DiaryUpdate) -> Diary:
    update_data = data.model_dump(exclude_unset=True)
    diary.update_from_dict(update_data)
    await diary.save()
    return diary


# Delete
async def delete(diary: Diary) -> None:
    await diary.delete()