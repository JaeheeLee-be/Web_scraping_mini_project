from typing import List
from fastapi import HTTPException, status
from app.repositories import quote_repo
from app.models.quote import Quote, Bookmark

# 1. 랜덤 명언 중 하나 선택
async def get_random_quote() -> Quote:
    quote = await quote_repo.get_random_quote()
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록된 명언이 없습니다."
        )
    return quote


# 2. 북마크 생성 (중복 확인 후 저장)
async def add_bookmark(user_id: int, quote_id: int) -> Bookmark:
    # 명언 존재 여부 확인
    quote = await Quote.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 명언을 찾을 수 없습니다."
        )

    # 중복 북마크 방지 (이미 있으면 에러 발생)
    is_exists = await Bookmark.filter(user_id=user_id, quote_id=quote_id).exists()
    if is_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 북마크에 추가된 명언입니다."
        )
    return await quote_repo.create_bookmark(user_id, quote_id)


# 3. 북마크 해제 (본인 확인 포함)
async def remove_bookmark(user_id: int, quote_id: int) -> None:
    # 해당 유저의 특정 북마크가 있는지 조회
    bookmark = await Bookmark.get_or_none(user_id=user_id, quote_id=quote_id)

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="북마크 정보를 찾을 수 없거나 이미 해제되었습니다."
        )
    await bookmark.delete()


# 4. 북마크 목록 (사용자가 고른 명언들만 조회)
async def get_my_bookmarks(user_id: int) -> List[Quote]:
    # Bookmark 레포지토리의 함수를 쓰거나 여기서 직접 filter 처리
    bookmarks = await Bookmark.filter(user_id=user_id).prefetch_related("quote")

    if not bookmarks:
        return []

    # 북마크 객체 리스트에서 연결된 Quote 객체만 뽑아서 반환
    return [b.quote for b in bookmarks]