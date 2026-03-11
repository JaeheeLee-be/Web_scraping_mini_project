from tortoise import fields, models


class Diary(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="diaries") # 한명의 유저가 여러 개의 일기 소유

    class Meta:
        db_table = "diaries"