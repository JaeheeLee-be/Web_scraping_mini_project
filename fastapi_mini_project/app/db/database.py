import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

DATABASE_URL = f"postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Aerich와 Tortoise가 공유하는 설정 딕셔너리
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            # 초기 마이그레이션을 위해 aerich.models를 포함합니다.
            "models": ["app.models.user", "aerich.models"],
            "default_connection": "default",
        }
    },
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

async def close_db():
    await Tortoise.close_connections()