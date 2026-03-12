# models -> quote.py

from tortoise import fields, models


class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=255)

    class Meta:
        table = "quotes"


class Bookmark(models.Model):
    user_id = fields.IntField()
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarks")

    class Meta:
        # 유저ID와 명언ID의 조합이 유일해야 함 (중복 방지)
        unique_together = (("user_id", "quote_id"),)