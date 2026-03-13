from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.database import TORTOISE_ORM
from app.api.v1 import auth, diary, quote
from app.scraping.quote_scraper import run_quote_scraper
from app.scraping.question_scraper import run_question_scraper
from app.models.quote import Quote
from app.models.question import Question

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    # 1. 명언 체크 및 수집
    current_quote = await Quote.all().count()
    required_quote = 45

    if current_quote < required_quote:
        print(f"현재 명언({current_quote}개)이 부족. 추가 수집을 시작...")
        quote_result = await run_quote_scraper(max_pages=5)
        print(f"스크랩: {quote_result}")
    else:
        print(f"이미 명언({current_quote}개)이 저장됨 건너뜀.")

    # 2. question 체크 및 수집
    current_question = await Question.all().count()
    required_question = 45

    if current_question < required_question:
        print(f"현재 질문({current_question}개)이 부족. 추가 수집 시작...")
        question_result = await run_question_scraper(max_pages=5)
        print(f"스크랩: {question_result}")
    else:
        print(f"이미 질문({current_question}개)이 저장됨 건너뜀")
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