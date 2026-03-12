from fastapi import FastAPI
from app.db.database import init_db, close_db
from app.api.v1 import auth, diary, quote
from app.scraping.quote_scraper import run_quote_scraper
from app.models.quote import Quote # DB 모델 추가

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1/quote")


@app.on_event("startup")
async def startup():
    await init_db()

    # 1. 현재 DB에 저장된 명언 개수 확인
    current_count = await Quote.all().count()

    # 한 페이지당 약 20개의 명언이 있다고 가정할 때,
    # 5페이지 분량(약 100개)보다 적으면 스크레이핑 실행
    REQUIRED_COUNT = 45

    if current_count < REQUIRED_COUNT:
        print(f"현재 명언({current_count}개)이 부족합니다. 추가 수집을 시작합니다...")
        # 부족한 양에 맞춰서 max_pages 조절 가능 (여기서는 고정 5페이지)
        result = await run_quote_scraper(max_pages=5)
        print(f"scraped: {result}")
    else:
        print(f"이미 명언({current_count}개)이 저장되어 있어 스크레이핑을 건너뜁니다.")

@app.on_event("shutdown")
async def shutdown():
    await close_db()
