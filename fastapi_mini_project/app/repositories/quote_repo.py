import random
from typing import List, Optional
from app.models.quote import Quote, Bookmark


# 1. 랜덤 명언 가져오기
async def get_random_quote() -> Optional[Quote]:
    # 전체 개수 확인
    count = await Quote.all().count()
    if count == 0:
        return None

    # 0 ~ (전체개수-1) 사이의 랜덤 인덱스 선택
    random_index = random.randint(0, count - 1)

    # offset을 사용하여 랜덤하게 선택된 하나를 가져옴
    return await Quote.all().offset(random_index).first()


# 2. 북마크 생성
async def create_bookmark(user_id: int, quote_id: int) -> Bookmark:
    return await Bookmark.create(user_id=user_id, quote_id=quote_id)


# 3. 명언 대량 생성 (스크래핑용으로 쓰일 함수)
async def bulk_create_quotes(quote_list: List[dict]):
    # dict 리스트를 Quote 모델 객체 리스트로 변환
    quotes = [Quote(content=q['content'], author=q['author']) for q in quote_list]
    # 한번에 insert (bulk_create)
    return await Quote.bulk_create(quotes)