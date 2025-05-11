from tortoise import fields, models

# Таблица тарифов: | Объем ГБ | Количество дней | Цена |
class DataBase_EsimPackageGlobal(models.Model):
    id = fields.IntField(pk=True)
    package_code = fields.CharField(max_length=20)  # Новый параметр
    gb = fields.FloatField()
    days = fields.IntField()
    price = fields.FloatField()

    countries: fields.ReverseRelation["DataBase_EsimCountryGlobal"]

    class Meta:
        table = "esim_global_package"


# Таблица стран по тарифам: | Страна | Код страны |
class DataBase_EsimCountryGlobal(models.Model):
    id = fields.IntField(pk=True)
    package = fields.ForeignKeyField("models.DataBase_EsimPackageGlobal", related_name="countries")
    location_name = fields.CharField(max_length=100)
    location_code = fields.CharField(max_length=10)

    class Meta:
        table = "esim_global_countries"