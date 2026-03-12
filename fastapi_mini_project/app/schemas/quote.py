from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


# 1. 명언 정보 기본 (조회용)
class QuoteResponse(BaseModel):
    id: int
    content: str
    author: str

    # DB 객체를 Pydantic으로 자동 변환하기 위한 설정
    model_config = ConfigDict(from_attributes=True)


# 2. 북마크 생성 시 요청 바디 (클라이언트 -> 서버)
class BookmarkCreate(BaseModel):
    quote_id: int


# 3. 북마크 결과 응답 (서버 -> 클라이언트)
class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    quote_id: int
    created_at: datetime  # 언제 북마크했는지 정보 포함 가능

    model_config = ConfigDict(from_attributes=True)


# 4. 내 북마크 목록 전체 응답 (메타데이터 포함 시)
class MyBookmarkListResponse(BaseModel):
    total: int
    bookmarks: List[QuoteResponse]  # 북마크한 명언들의 실제 내용 리스트

    model_config = ConfigDict(from_attributes=True)