from database.models.esim_order import EsimOrder
from database.models.user import DataBase_User
from api.microservices.order_esim import order_esim
from dateutil import parser


async def create_esim_order(user: DataBase_User, package_code: str, price) -> EsimOrder:
    # Шаг 1: сделать заказ через eSIM API
    api_response = await order_esim(package_code=package_code, price=price)
    order_data = api_response.get("data")

    if not order_data:
        raise Exception("Нет данных заказа от eSIM API")

    # Шаг 2: сохранить заказ в БД
    order = await EsimOrder.create(
        order_no=order_data["orderNo"],
        user=user,
        transaction_id=order_data.get("transactionId"),
        package_code=package_code,
        iccid=order_data["iccid"],
        imsi=order_data["imsi"],
        ac=order_data["ac"],
        qr_code_url=order_data["qrCodeUrl"],
        smdp_status=order_data["smdpStatus"],
        active_type=order_data["activeType"],
        expired_time=parser.isoparse(order_data["expiredTime"]),
        total_volume=order_data["totalVolume"],
        order_usage=order_data["orderUsage"],
        duration_unit=order_data.get("durationUnit", "DAY")
    )

    return order