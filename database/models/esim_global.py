from tortoise import fields, models

# Таблица тарифов: | Объем ГБ | Количество дней | Цена |
class DataBase_EsimPackageGlobal(models.Model):
    id = fields.IntField(pk=True)
    gb = fields.FloatField()  # Объем данных в ГБ
    days = fields.IntField()  # Количество дней
    price = fields.FloatField()  # Цена

    countries: fields.ReverseRelation["DataBase_EsimCountryGlobal"]

    class Meta:
        table = "esim_package_global"


# Таблица стран по тарифам: | Страна | Код страны |
class DataBase_EsimCountryGlobal(models.Model):
    id = fields.IntField(pk=True)
    package = fields.ForeignKeyField("models.DataBase_EsimPackageGlobal", related_name="countries")
    location_name = fields.CharField(max_length=100)
    location_code = fields.CharField(max_length=10)

    class Meta:
        table = "esim_countries_global"