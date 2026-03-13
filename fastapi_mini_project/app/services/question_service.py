from app.repositories import question_repo
from fastapi import HTTPException


async def pick_daily_question(user_id: int):
    question = await question_repo.get_random_question(user_id)

    if not question:
        raise HTTPException(status_code=404, detail="새로운 질문 없음")

    return question


async def register_question(user_id: int, question_id: int):
    return await question_repo.save_user_question (user_id, question_id)