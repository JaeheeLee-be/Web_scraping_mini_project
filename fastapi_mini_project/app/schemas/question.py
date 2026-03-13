from pydantic import BaseModel


class Question(BaseModel):
    id: int
    question: str

    class Config:
        from_attributes = True


class UserQuestion(BaseModel):
    question_id: int

