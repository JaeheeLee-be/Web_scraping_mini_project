from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings

app = FastAPI()


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