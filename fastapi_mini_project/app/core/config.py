from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM : str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINS : int = 30