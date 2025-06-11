from tortoise import fields, models


class EsimOrder(models.Model):
    order_no = fields.CharField(max_length=32, pk=True)
    user = fields.ForeignKeyField("models.DataBase_User", related_name="orders")

    transaction_id = fields.CharField(max_length=64, null=True)
    slug = fields.CharField(max_length=20)

    price = fields.FloatField(null=True)
    count = fields.IntField(null=True)
    amount = fields.BigIntField(null=True)

    iccid = fields.CharField(max_length=32, null=True)
    imsi = fields.CharField(max_length=32, null=True)
    msisdn = fields.CharField(max_length=32, null=True)
    sms_status = fields.IntField(null=True)

    ac = fields.TextField()
    qr_code_url = fields.TextField()
    short_url = fields.TextField(null=True)

    smdp_status = fields.CharField(max_length=32, null=True)
    active_type = fields.IntField(null=True)
    data_type = fields.IntField(null=True)

    activate_time = fields.DatetimeField(null=True)
    expired_time = fields.DatetimeField()

    total_volume = fields.BigIntField(null=True)
    total_duration = fields.IntField(null=True)
    duration_unit = fields.CharField(max_length=10, null=True)
    order_usage = fields.BigIntField(null=True)

    esim_status = fields.CharField(max_length=32, null=True)
    pin = fields.CharField(max_length=16, null=True)
    puk = fields.CharField(max_length=16, null=True)
    apn = fields.CharField(max_length=100, null=True)

    package_list = fields.JSONField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "esim_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order({self.order_no})"
