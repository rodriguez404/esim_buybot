from tortoise import fields, models


class EsimOrder(models.Model):
    order_no = fields.CharField(max_length=32, pk=True)
    user = fields.ForeignKeyField("models.DataBase_User", related_name="orders")

    transaction_id = fields.CharField(max_length=64, null=True)
    slug = fields.CharField(max_length=20)

    iccid = fields.CharField(max_length=32, null=True)  # nullable
    imsi = fields.CharField(max_length=32, null=True)   # nullable
    ac = fields.TextField()
    qr_code_url = fields.TextField()

    smdp_status = fields.CharField(max_length=32)
    active_type = fields.IntField()

    expired_time = fields.DatetimeField()
    total_volume = fields.BigIntField()
    order_usage = fields.BigIntField(null=True)  # nullable
    duration_unit = fields.CharField(max_length=10, null=True)  # nullable

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "esim_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order({self.order_no})"