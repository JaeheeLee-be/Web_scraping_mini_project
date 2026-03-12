# app/models/user.py
from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    nickname = fields.CharField(max_length=50, unique=True) # 스키마의 nickname과 매칭함
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    password_hash = fields.CharField(max_length=128, null=True) # 비밀번호는 해싱해서 저장함

    class Meta:
        table = "users"


class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="token_blacklist")
    expired_at = fields.DatetimeField()

    class Meta:
        table = "token_blacklist"

