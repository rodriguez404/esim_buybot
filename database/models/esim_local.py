from tortoise import fields, models


# Таблица местных стран: | Страны | Код страны |
class DataBase_LocalCountry(models.Model):
    id = fields.IntField(pk=True)
    location_name = fields.CharField(max_length=100)
    location_code = fields.CharField(max_length=10)

    tariffs: fields.ReverseRelation["DataBase_LocalTariff"]

    class Meta:
        table = "esim_local_countries"


# Таблица тарифов для стран: | Объем ГБ | Количество дней | Цена |
class DataBase_LocalTariff(models.Model):
    id = fields.IntField(pk=True)
    country = fields.ForeignKeyField("models.DataBase_LocalCountry", related_name="tariffs")

    slug = fields.CharField(max_length=20, unique=True)
    gb = fields.FloatField()
    days = fields.IntField()
    price = fields.FloatField()

    class Meta:
        table = "esim_local_tariffs"