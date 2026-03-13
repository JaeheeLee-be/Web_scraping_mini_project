from fastapi import APIRouter, HTTPException, Depends
from app.services.question_service import pick_daily_question, register_question
from app.schemas.question import Question, UserQuestion

from app.models.user import User
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/question", tags=["Question"])

# 1. 랜덤 질문 들고오기
@router.get("/daily")
async def get_random_question(current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    question = await pick_daily_question(user_id)
    if not question:
        raise HTTPException(status_code=404, detail="질문 없음")
    return question

