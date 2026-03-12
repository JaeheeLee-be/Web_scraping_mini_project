import re
from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

class CreateUser(BaseModel):
    nickname : str = Field(min_length=2)
    password : str
    email : EmailStr


    @field_validator("password")
    @classmethod
    def password_validator(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError("올바른 방식으로 입력하세요.")
        return v

class LoginUser(BaseModel):
    email : EmailStr
    password : str

class ResponseUser(BaseModel):
    id: int
    nickname: str
    email: EmailStr

    model_config = {
        "from_attributes": True   ####  from_attributes 사용 이유: FastAPI와 Tortoise ORM 사용시 발생할 수 있는 충돌 방지
    }


class RefreshTokenRequest(BaseModel):
    refresh_token : str = Field(..., description="재발급용 토큰")

class TokenResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class UpdateUser(BaseModel):
    nickname : str | None = Field(default=None, min_length=2)
    email : EmailStr | None = None

class UpdatePassword(BaseModel):
    current_password : str
    new_password : str
    new_password_confirm : str

    @field_validator("new_password")
    @classmethod
    def new_password_validator(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError("올바른 방식으로 입력하세요.")
        return v

    @model_validator(mode="after")
    def confirm_validator(self):
        if self.new_password != self.new_password_confirm:
            raise ValueError("동일한 비밀번호를 입력하세요.")
        return self