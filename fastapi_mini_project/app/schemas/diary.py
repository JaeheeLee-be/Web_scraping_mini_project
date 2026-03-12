from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DiaryBase(BaseModel):
    title: str = Field(..., max_length=50, description="제목을 입력하세요.")
    content: str = Field(..., description="내용을 입력하세요.")


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    content: Optional[str] = None


class DiaryResponse(DiaryBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DiaryListResponse(BaseModel):
    total: int
    page: int
    size: int
    diaries: list[DiaryResponse]