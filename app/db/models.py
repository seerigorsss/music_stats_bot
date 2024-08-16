from tortoise import fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = 'users'

    # User settings
    user_id = fields.BigIntField(pk=True, unique=True)
    status = fields.CharField(max_length=16, null=True, default=None)
    username = fields.CharField(max_length=64, null=True, default=None)
    referer_login = fields.TextField(null=True)
    language_code = fields.TextField(null=True)
    registration_date = fields.DatetimeField(null=True)
    last_active = fields.DatetimeField(null=True)
