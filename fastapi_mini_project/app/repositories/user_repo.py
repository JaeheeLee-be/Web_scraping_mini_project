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