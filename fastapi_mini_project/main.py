from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.database import TORTOISE_ORM
from app.api.v1 import auth, diary, quote
from app.scraping.quote_scraper import run_quote_scraper
from app.models.quote import Quote

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    current_count = await Quote.all().count()
    REQUIRED_COUNT = 45

    if current_count < REQUIRED_COUNT:
        print(f"현재 명언({current_count}개)이 부족합니다. 추가 수집을 시작합니다...")
        result = await run_quote_scraper(max_pages=5)
        print(f"scraped: {result}")
    else:
        print(f"이미 명언({current_count}개)이 저장되어 있어 스크레이핑을 건너뜁니다.")

@app.get("/")
def read_root():
    return {"message": "hello"}

@app.get("/health")
def health():
    return {"status": "ok"}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)