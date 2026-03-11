from tortoise import fields, models


class Quote(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    author = fields.CharField(max_length=255)

    class Meta:
        table = "quotes"


class Bookmark(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="bookmarks")
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarks")

    class Meta:
        table = "bookmarks"