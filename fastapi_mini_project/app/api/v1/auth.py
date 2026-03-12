from fastapi import APIRouter, Depends
from app.services.auth_service import register, login, logout, get_me, refresh, update_user, update_password
from app.core.security import get_current_user, oauth2_scheme
from app.schemas.user import UpdateUser, CreateUser, LoginUser, RefreshTokenRequest, UpdatePassword


router = APIRouter()

@router.post("/register")
async def create_user(user_data: CreateUser):
    return await register(user_data)

@router.post("/login")
async def user_login(user_data: LoginUser):
    return await login(user_data)

@router.post("/logout")
async def user_logout(
        token: str = Depends(oauth2_scheme),
        current_user = Depends(get_current_user)
):
    return await logout(token, current_user)

@router.get("/me")
async def user_me(current_user = Depends(get_current_user)):
    return await get_me(current_user)

@router.post("/refresh")
async def refresh_token(data: RefreshTokenRequest):
    return await refresh(data)

@router.patch("/me")
async def patch_user(data:UpdateUser, current_user = Depends(get_current_user)):
    return await update_user(current_user, data)

@router.patch("/me/password")
async def patch_password(data:UpdatePassword, current_user = Depends(get_current_user)):
    return await update_password(current_user, data)