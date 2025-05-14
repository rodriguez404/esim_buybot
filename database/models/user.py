from tortoise import fields, models

class DataBase_User(models.Model):
    id = fields.BigIntField(pk=True)  # Telegram ID
    username = fields.CharField(max_length=100, null=True)
    language = fields.CharField(max_length=5, default="ru")  # Язык пользователя
    registered_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user"

    def __str__(self):
        return f"User({self.id})"