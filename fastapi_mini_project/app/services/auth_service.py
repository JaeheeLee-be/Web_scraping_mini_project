from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password
from app.repositories.user_repo import get_user_email, get_user_nickname, create_user
from app.schemas.user import CreateUser, LoginUser

from fastapi_mini_project.app.core.security import verify_password


async def register(user_data: CreateUser):
    response_email = await get_user_email(user_data.email)

    if response_email:
        raise HTTPException(status_code=401, detail="이미 존재하는 이메일입니다.")

    response_nickname = await get_user_nickname(user_data.nickname)

    if response_nickname:
        raise HTTPException(status_code=401, detail="이미 존재하는 아이디입니다.")

    hashed_password = get_password_hash(user_data.password)

    return await create_user(
        email=user_data.email,
        nickname=user_data.nickname,
        hashed_password=hashed_password
    )

async def login(user_data: LoginUser):
    response_email = await get_user_email(user_data. email)

    if not response_email:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")

    hashed_password = verify_password(user_data.password)