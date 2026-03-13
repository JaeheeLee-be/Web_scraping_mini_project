from fastapi import APIRouter, HTTPException
from starlette import status

from app.services.question_service import pick_daily_question, register_question
from app.schemas.question import Question, UserQuestion


router = APIRouter(prefix="/question", tags=["question"])

# 1. 랜덤 질문 들고오기
@router.get("/daily", response_model=Question)
async def get_random_question(user_id: int):
    question = await pick_daily_question(user_id)
    if not question:
        raise HTTPException(status_code=404, detail="질문 없음")
    return question

# 2.질문 선택. 등록
@router.post("/pick_daily_question", response_model=Question)
async def select_question(data: UserQuestion, user_id: int):
    try:
        await register_question(user_id, data.question_id)
        return {"message": "등록 완료"}
    except Exception as e:
        # 이미 등록된 질문일 경우 등에 대한 예외 처리
        raise HTTPException(status_code=400, detail="등록된 질목 혹은 오류.")