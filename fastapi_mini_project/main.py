from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings
from app.api.v1 import auth, diary, quote
app = FastAPI()


app.include_router(auth.router,  prefix="/api/v1/auth",  tags=["Auth"])
app.include_router(diary.router, prefix="/api/v1")
app.include_router(quote.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "hello"}


@app.get("/health")
def health():
    return {"status": "ok"}


register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)