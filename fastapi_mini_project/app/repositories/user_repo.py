from app.models.user import User, TokenBlacklist


async def get_user_id(user_id: int):
    return await User.get_or_none(id=user_id)

async def get_user_email(email: str):
    return await User.get_or_none(email=email)

async def get_user_nickname(nickname: str):
    return await User.get_or_none(nickname=nickname)

async def create_user(nickname: str, email: str, password_hash: str):
    return await User.create(
        nickname=nickname, email=email, password_hash=password_hash
    )

async def add_token_blacklist(token: str, user_id: int, expired_at):
    return await TokenBlacklist.create(
        token=token,
        user_id=user_id,
        expired_at=expired_at
    )

async def get_token_blacklist(token: str):
    return await TokenBlacklist.get_or_none(token=token)

async def get_update_user(current_user, data):
    await current_user.update_from_dict(data.model_dump(exclude_none=True))
    await current_user.save()
    return current_user

async def get_update_password(current_user, data):
    current_user.password_hash = data
    await current_user.save()
    return current_user