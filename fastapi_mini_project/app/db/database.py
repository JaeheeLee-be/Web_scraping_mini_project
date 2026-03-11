import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DATABASE_URL = f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Aerich와 Tortoise가 공유하는 설정 딕셔너리
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL}, # 이미 os.getenv를 통해 url을 만들어서 settings.가 필요하지 않음
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.diary",
                "app.models.quote",
                "app.models.question",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

async def close_db():
    await Tortoise.close_connections()