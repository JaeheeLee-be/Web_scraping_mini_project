from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.core.config import settings
from app.db.database import TORTOISE_ORM
from app.api.v1 import diary, auth, question, quote


app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(diary.router, prefix="/api/v1")
# app.include_router(question.router, prefix="/api/v1")
# app.include_router(quote.router, prefix="/api/v1")

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