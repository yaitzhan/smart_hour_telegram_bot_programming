from tortoise.models import Model
from tortoise import fields


class TelegramUser(Model):
    user_id = fields.CharField(max_length=255, unique=True)
    phone_number = fields.CharField(max_length=255, null=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    authorized = fields.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.user_id)

    class Meta:
        table = 'telegramuser'
