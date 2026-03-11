# 토큰을 헤더에 담는 이유
# 웹 표준
# HTTP 표준에서 인증 토큰을 authorization 헤더에 포함하여 서버로 보내는 방식을 권장합니다.
# Bearer는 authorization 헤더에서 인증 수단의 일종이며, 사용자를 대표하는 접근 권한을 부여받았음을 의미합니다.
# (= 이 토큰을 소지한 사람에게 접근 권한이 있다) OAuth 2.0에서도 사용하는 웹 인증 표준에서 가장 널리 사용되는 방식입니다.
# 보안 강화
# 토큰을 헤더에 담으면 서버가 HttpOnly 쿠키나 보안 조치와 함께 보호가 가능합니다.
# 또한, CSRF 방지 및 토큰을 URL에 포함할 경우 북마크, 공유, 보안 문제가 발생합니다
# 출처: https://kyung-a.tistory.com/64#왜_토큰을_HTTP_header에_담아야_하는가? [개발로그:티스토리]
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.util import deprecated



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 예시
# SECRET_KEY = "ozbe17_super_long_and_complicate_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINS = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# rebase 내 분기 1 팀장님 pr 2 내 기능 브런치 = 1 로컬의 develop == header