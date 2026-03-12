from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.schemas.user import CreateUser, LoginUser, TokenResponse
from app.repositories.user_repo import get_user_email, get_user_nickname, create_user

from fastapi_mini_project.app.core.security import decode_token
from fastapi_mini_project.app.models.user import TokenBlacklist
from fastapi_mini_project.app.repositories.user_repo import add_token_blacklist


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
        password_hash=hashed_password
    )

async def login(user_data: LoginUser):
    response_email = await get_user_email(user_data. email)

    if not response_email:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")

    if not verify_password(user_data.password, response_email.password_hash):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    access_token = create_access_token(data={"sub": str(response_email.id)})
    refresh_token = create_refresh_token(data={"sub": str(response_email.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

async def logout(user_data: current_user):
    payload = decode_token(token)
    expire_at = payload.get("exp")

    await add_token_blacklist(
        token=token,
        user_id=current_user

    )