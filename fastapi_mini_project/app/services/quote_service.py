# 1. 랜덤 명언 중 하나 선택
# 2. 북마크 생성 -> 중복 확인 후 저장
# 3. 북마크 해제 -> 북마크 한 본인인지 확인
# 4. 북마크 목록 -> 사용자가 고른 명언들만 조회

from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories import quote_repo
from app.models.quote import Quote, Bookmark


# 1. 랜덤 명언 제공
async def get_random_quote() -> Optional[Quote]:
    quote = await quote_repo.get_random_quote()
    if not quote:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,
                             detail = "등록된 명언이 없음")
    return quote

# 2. 명언 북마크 추가 로직
async def add_bookmark(user_id: int, quote_id: int) -> Bookmark:
    # 명언 존재 확인
    quote = await Quote.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,
                             detail = "해당 명언을 찾을 수 없음")

    # 중복 북마크 방지
    is_exists = await Bookmark.filter(user_id=user_id, quote_id=quote_id).exists()
    if not is_exists:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,
                             detail = "이미 추가된 명언")
    return await quote_repo.create_bookmark(user_id, quote_id)


# 3. 북마크 해체
async def remove_bookmark(user_id: int, quote_id: int) -> None:
    bookmark = await Bookmark.get_or_none(user_id=user_id, quote_id=quote_id)
    if not bookmark:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND,
                             detail = "북마크 정보 찾기 실패")
    await bookmark.delete()

# 4. 사용자의 북마크 리스트 조회
async def get_my_bookmakrs(user_id: int) -> List[Quote]:
    # 사용자의 북마크에서 quote 정보만 가져옴
    bookmakrs = await Bookmark.filter(user_id=user_id).prefetch_related("quote")
    return [b.quote for b in bookmakrs]