from tortoise import fields, models


class Question(models.Model):
    id = fields.IntField(pk=True)
    question_text = fields.TextField()

    class Meta:
        table = "questions"


class UserQuestion(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="user_questions")
    question = fields.ForeignKeyField("models.Question", related_name="user_questions")

    class Meta:
        table = "user_questions"
