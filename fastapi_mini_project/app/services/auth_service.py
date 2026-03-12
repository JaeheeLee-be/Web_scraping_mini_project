from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token, verify_refresh_token
from app.schemas.user import CreateUser, LoginUser, TokenResponse, ResponseUser, RefreshTokenRequest, UpdateUser, UpdatePassword
from app.repositories.user_repo import get_user_email, get_user_nickname, create_user, add_token_blacklist, get_token_blacklist, get_update_user, get_update_password
from fastapi import HTTPException
from datetime import datetime, timezone

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
    response_email = await get_user_email(user_data.email)

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

async def logout(token: str, current_user):
    payload = decode_token(token)
    expire_at = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)

    await add_token_blacklist(
        token=token,
        user_id=current_user.id,
        expired_at=expire_at
    )

async def get_me(current_user):
    return ResponseUser(
        id=current_user.id,
        nickname=current_user.nickname,
        email=current_user.email
    )

async def refresh(data: RefreshTokenRequest):
    blacklist = await get_token_blacklist(data.refresh_token)

    if blacklist:
        raise HTTPException(status_code=401, detail="이미 만료된 토큰입니다.")

    payload = verify_refresh_token(data.refresh_token)

    user_id = payload.get("sub")
    new_access_token = create_access_token(data={"sub": user_id})

    return {"access_token": new_access_token}

async def update_user(current_user, data: UpdateUser):
    return await get_update_user(current_user, data)

async def update_password(current_user, data: UpdatePassword):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=401, detail="현재 비밀번호가 일치하지 않습니다.")

    new_hash = get_password_hash(data.new_password)
    return await get_update_password(current_user, new_hash)