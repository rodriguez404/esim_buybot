from tortoise import fields, models

# Таблица групп
class TariffGroup(models.Model):
    id = fields.IntField(pk=True)
    countries = fields.JSONField()  # ["TR"], ["AU", "JP"]
    tariff_prices = fields.JSONField()  # [0.46, 1.39, ...]
    name = fields.CharField(max_length=100) # опциональные названия для групп
    
    class Meta:
        table = "admin_tariff_groups"