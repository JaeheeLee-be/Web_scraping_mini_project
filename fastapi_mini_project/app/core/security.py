# ─── 토큰을 Authorization 헤더에 담는 이유 ───
# HTTP 표준에서 인증 토큰은 Authorization 헤더에 포함하는 방식을 권장
# "Bearer 토큰" = 이 토큰을 소지한 사람에게 접근 권한을 부여한다는 의미
# URL에 토큰을 포함하면 브라우저 히스토리·로그·북마크 등에 노출되어 보안 위험 발생
# 헤더에 담으면 HTTPS 암호화 적용, CSRF 공격 방어에도 유리

from datetime import datetime, timedelta, timezone
# python-jose 라이브러리: JWT 생성(encode)·검증(decode)·에러 처리를 담당
from jose import JWTError, jwt
# passlib: 비밀번호 해싱 라이브러리. CryptContext로 여러 알고리즘을 관리 가능
from passlib.context import CryptContext
# Depends: FastAPI 의존성 주입 - 함수 파라미터로 넣으면 자동으로 실행되어 값을 주입
# HTTPException: HTTP 에러 응답을 발생시키는 FastAPI 기본 예외
from fastapi import Depends, HTTPException
# HTTPBearer: Authorization 헤더에서 Bearer 토큰을 추출하는 보안 스킴
# → Swagger UI에서 자물쇠 아이콘 클릭 → 토큰 입력하는 방식으로 연결됨
# HTTPAuthorizationCredentials: HTTPBearer가 반환하는 객체 (scheme + credentials 포함)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.models.user import User

# bcrypt 알고리즘으로 비밀번호 해싱 컨텍스트 설정
# deprecated="auto": 오래된 해시 방식은 자동으로 최신 방식으로 재해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTPBearer 인스턴스: 각 요청의 Authorization 헤더에서 토큰을 자동 추출
# OAuth2PasswordBearer 대신 HTTPBearer를 쓰는 이유:
#   OAuth2는 Swagger에서 폼(username/password)으로 토큰 획득 시도 → 우리 API는 JSON 방식이라 불일치
#   HTTPBearer는 단순히 "토큰 값 직접 입력" 방식 → Swagger와 잘 맞음
oauth2_scheme = HTTPBearer()


def get_password_hash(password: str) -> str:
    # 평문 비밀번호를 bcrypt로 해싱해서 반환
    # bcrypt는 단방향 해시 → 원래 비밀번호를 복원 불가능
    # 해시값에 salt(랜덤값)가 포함되어 있어 같은 비밀번호도 매번 다른 해시 생성
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 입력된 평문 비밀번호와 DB에 저장된 해시를 비교
    # 내부적으로 hash에서 salt를 추출해서 동일한 방식으로 해싱 후 비교
    return pwd_context.verify(plain_password, hashed_password)

def verify_refresh_token(token: str) -> dict:
    # Refresh Token의 유효성 검증 후 payload(데이터) 반환
    # SECRET_KEY로 서명 검증 + 만료 시간 자동 확인
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # 서명 불일치, 만료, 형식 오류 등 모든 JWT 에러를 401로 처리
        raise HTTPException(status_code=401, detail="유효하지 않는 Refresh Token입니다.")

def create_access_token(data: dict) -> str:
    # Access Token 생성 (짧은 만료 시간 - 기본 30분)
    to_encode = data.copy()  # 원본 dict 수정 방지를 위해 복사
    # timezone.utc: 시간대 정보를 포함한 현재 UTC 시간 (aware datetime)
    # timedelta: 만료 시간 계산에 사용
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})  # JWT 표준 "exp" 클레임 추가
    # jwt.encode: payload를 SECRET_KEY로 서명하여 JWT 문자열 반환
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    # Refresh Token 생성 (긴 만료 시간 - 기본 30일)
    # Access Token이 만료됐을 때 이 토큰으로 새 Access Token을 재발급받음
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    # JWT를 검증하고 내부 데이터(payload)를 반환
    # SECRET_KEY로 서명 검증 + 만료 시간 자동 확인
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않는 토큰입니다.")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    # FastAPI 의존성 주입 함수: 요청에서 토큰을 꺼내 현재 로그인 유저 객체를 반환
    # Depends(oauth2_scheme): 요청의 Authorization 헤더에서 Bearer 토큰 자동 추출
    # credentials.credentials: 실제 토큰 문자열 (Bearer 제거 후 순수 토큰만)
    token = credentials.credentials

    payload = decode_token(token)      # 토큰 유효성 검증 + payload 추출
    user_id = payload.get("sub")       # "sub" 클레임에서 user_id 꺼냄 (토큰 생성 시 저장한 값)

    if user_id is None:
        raise HTTPException(status_code=401, detail="유효하지 않는 토큰입니다.")

    # DB에서 실제 유저 조회 (탈퇴한 유저의 토큰 사용 방지)
    # get_or_none: 없으면 None 반환 (get은 없으면 예외 발생)
    user = await User.get_or_none(id=int(user_id))

    if user is None:
        raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")

    return user  # 라우터에서 current_user = Depends(get_current_user)로 받아서 사용