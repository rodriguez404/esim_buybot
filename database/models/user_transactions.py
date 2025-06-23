from tortoise import fields, models

# Таблица тарифов: | Объем ГБ | Количество дней | Цена |
class DataBase_UserTransactions(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    package_code = fields.CharField(max_length=20)
    count = fields.IntField()
    date = fields.DatetimeField()
    orderNo = fields.CharField(max_length=20)
    transactionId = fields.CharField(max_length=20)

    class Meta:
        table = "user_transactions"