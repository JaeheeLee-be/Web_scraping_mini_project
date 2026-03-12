from fastapi import FastAPI
from app.db.database import init_db, close_db
from app.api.v1 import auth, diary, quote
from app.scraping.quote_scraper import run_quote_scraper

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/vi/quote")

@app.on_event("startup")
async def startup():
    await init_db()

    result = await run_quote_scraper(max_pages=3)
    print(f"scraped: {result}")

@app.on_event("shutdown")
async def shutdown():
    await close_db()
