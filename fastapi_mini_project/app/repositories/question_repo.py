#question_repo.py
from app.models.question import Question, UserQuestion
from tortoise.expressions import RawSQL


async def get_random_question(user_id: int):
    # 1. 사용자가 선택한 질문 ID 목록 가져오기
    pick_ids = await UserQuestion.filter(user_id=user_id).values_list("question_id", flat=True)

    # 2. 선택 안한 질문 랜덤 1개 뽑기
    query = Question.filter(id__not_in=pick_ids)

    return await query.annotate(random=RawSQL("RANDOM()")).order_by("random").first()


async def save_user_question(user_id: int, question_id: int):
    return await UserQuestion.create(user_id=user_id, question_id=question_id)

async def bulk_create_questions(data_list: list):
    question_objs = [
        Question(question_text=item['content'])
        for item in data_list
    ]
    await Question.bulk_create(question_objs, ignore_conflicts=True)
