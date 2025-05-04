from tortoise import fields, models


# Таблица регионов: | Регионы |
class DataBase_Region(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)  # Название региона

    tariffs: fields.ReverseRelation["DataBase_RegionalTariff"]

    class Meta:
        table = "esim_regions"


# Таблица тарифов для регионов: | Объем ГБ | Количество дней | Цена |
class DataBase_RegionalTariff(models.Model):
    id = fields.IntField(pk=True)
    region = fields.ForeignKeyField("models.DataBase_Region", related_name="tariffs")
    gb = fields.FloatField()
    days = fields.IntField()
    price = fields.FloatField()

    countries: fields.ReverseRelation["DataBase_RegionalCountry"]

    class Meta:
        table = "esim_regional_tariffs"


# Таблица стран по региональным тарифам: | Страны | Код страны |
class DataBase_RegionalCountry(models.Model):
    id = fields.IntField(pk=True)
    region = fields.ForeignKeyField("models.DataBase_Region", related_name="region_countries")
    tariff = fields.ForeignKeyField("models.DataBase_RegionalTariff", related_name="country_links")

    location_name = fields.CharField(max_length=100)
    location_code = fields.CharField(max_length=10)

    class Meta:
        table = "esim_regional_countries"