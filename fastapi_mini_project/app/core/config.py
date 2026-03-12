# pydantic-settings 라이브러리에서 환경변수 관리 클래스를 가져옴
# BaseSettings: .env 파일이나 환경변수를 자동으로 읽어서 클래스 필드에 매핑해주는 Pydantic 기반 클래스
# SettingsConfigDict: .env 파일 경로, 인코딩 등 설정 옵션을 정의하는 딕셔너리 타입
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT 서명에 사용할 비밀키 (절대 외부에 노출되면 안 됨 → .env에서만 관리)
    SECRET_KEY: str

    # JWT 서명 알고리즘 (HS256 = HMAC + SHA256, 대칭키 방식으로 서버만 검증 가능)
    ALGORITHM: str = "HS256"

    # Access Token 만료 시간(분) - 짧게 유지해서 탈취 피해를 최소화
    ACCESS_TOKEN_EXPIRE_MINS: int = 30

    # Refresh Token 만료 시간(일) - Access Token 재발급 용도, 길게 유지
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Tortoise ORM 연결에 사용할 DB URL
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",            # 환경변수를 읽어올 파일 경로
        env_file_encoding="utf-8",  # 한글 등 특수문자를 위한 인코딩 설정
        extra="ignore",             # .env에 Settings에 없는 변수(POSTGRES_*)가 있어도 에러 없이 무시
    )

# 앱 전체에서 settings.SECRET_KEY 처럼 사용할 수 있도록 인스턴스를 모듈 레벨에서 생성
settings = Settings()