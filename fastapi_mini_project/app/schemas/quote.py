from pydantic import BaseModel, Field
from typing import Optional, List

# 1. 명언 기본 구조
class QuoteBase(BaseModel):
    content: str = Field(..., description="명언 내용을 입력하세요.")
    author: str = Field(..., max_length=255, description="저자 이름을 입력하세요.")


# 2. 명언 응답 (조회 시 사용)
class QuoteResponse(QuoteBase):
    id: int


    class Config:
        from_attributes = True

# 3. 북마크 생성을 위한 입력
class BookmarkCreate(BaseModel):
    quote_id: int = Field(..., description="북마크할 명언의 ID")


# 4. 명언 목록 응답 (DiaryListResponse와 동일한 스타일)
class QuoteListResponse(BaseModel):
    total: int = Field(..., description="전체 데이터 개수")
    page: int = Field(..., description="현재 페이지 번호")
    size: int = Field(..., description="페이지당 데이터 개수")
    quotes: List[QuoteResponse] = Field(..., description="명언 목록")


# 5. 북마크 응답 (사용자의 북마크 조회 시 사용)
class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    quote: QuoteResponse

    class Config:
        from_attributes = True