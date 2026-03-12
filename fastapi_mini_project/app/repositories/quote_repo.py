import random
from typing import List, Optional, Dict
from app.models.quote import Quote, Bookmark


# 1. 스크레이퍼용: 명언 대량 저장
async def bulk_create_quotes(quote_list: List[Dict[str, str]]):

    quote_objs = [
        Quote(content=item["content"], author=item["author"])
        for item in quote_list
    ]
    # bulk_create를 사용해 성능 최적화
    await Quote.bulk_create(quote_objs, ignore_conflicts=True)


# 2. 서비스용: 랜덤 명언 한 개 가져오기
async def get_random_quote() -> Optional[Quote]:

    count = await Quote.all().count()
    if count == 0:
        return None

    # 랜덤한 위치(offset)를 정해서 하나만 가져옴
    random_index = random.randint(0, count - 1)
    return await Quote.all().offset(random_index).first()


# 3. 서비스용: 북마크 생성
async def create_bookmark(user_id: int, quote_id: int) -> Bookmark:

    return await Bookmark.create(user_id=user_id, quote_id=quote_id)


# 4. 서비스용: 특정 유저의 북마크 목록 조회 (명언 포함)
async def get_bookmarks_by_user(user_id: int) -> List[Bookmark]:

    return await Bookmark.filter(user_id=user_id).prefetch_related("quote").all()