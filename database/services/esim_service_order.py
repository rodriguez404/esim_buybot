from database.models.esim_order import EsimOrder
from database.models.user import DataBase_User
from api.microservices.order_esim import order_esim
from api.microservices.get_order_details import get_esim_by_iccid
from dateutil import parser


async def create_esim_order(user: DataBase_User, slug: str, price) -> EsimOrder:
    # Шаг 1: сделать заказ через eSIM API
    api_response = await order_esim(slug=slug, price=price)
    order_data = api_response

    if not order_data:
        raise Exception("Нет данных заказа от eSIM API")

    # Шаг 2: сохранить заказ в БД
    order = await EsimOrder.create(
        order_no=order_data["orderNo"],
        user=user,
        transaction_id=order_data.get("transactionId"),
        slug=slug,
        iccid=order_data.get("iccid"),
        imsi=order_data.get("imsi"),
        ac=order_data["ac"],
        qr_code_url=order_data["qrCodeUrl"],
        smdp_status=order_data["smdpStatus"],
        active_type=order_data["activeType"],
        expired_time=parser.isoparse(order_data["expiredTime"]),
        total_volume=order_data["totalVolume"],
        order_usage=order_data.get("orderUsage", 0),  # По умолчанию 0
        duration_unit=order_data.get("durationUnit", "DAY")
    )

    return order

async def esim_profile_by_iccid(
    user: DataBase_User,
    iccid: str,
    page_num: int = 1,
    page_size: int = 20,
) -> EsimOrder:
    """
    1) Получить профиль eSIM по ICCID
    2) Создать или обновить запись в БД с полным списком полей
    """
    # 1) Fetch from API
    profile = await get_esim_by_iccid(iccid=iccid, page_num=page_num, page_size=page_size)

    # 2) Собираем данные из ответа
    # В profile лежит словарь примерно такого вида:
    # {
    #   "orderNo": "...",
    #   "transactionId": "...",
    #   "imsi": "...",
    #   "iccid": "8943108170000775671",
    #   "msisdn": "...",
    #   "smsStatus": 1,
    #   "ac": "...",
    #   "qrCodeUrl": "...",
    #   "shortUrl": "...",
    #   "smdpStatus": "...",
    #   "activeType": 0,
    #   "dataType": 1,
    #   "activateTime": null,
    #   "expiredTime": "...",
    #   "totalVolume": 5368709120,
    #   "totalDuration": 30,
    #   "durationUnit": "DAY",
    #   "orderUsage": 0,
    #   "esimStatus": "...",
    #   "pin": "",
    #   "puk": "",
    #   "apn": "drei.at",
    #   "packageList": [ {...}, ... ]
    # }
    order_no       = profile["orderNo"]
    transaction_id = profile.get("transactionId")
    imsi           = profile.get("imsi")
    msisdn         = profile.get("msisdn")
    sms_status     = profile.get("smsStatus")
    ac             = profile.get("ac")
    qr_code_url    = profile.get("qrCodeUrl")
    short_url      = profile.get("shortUrl")
    smdp_status    = profile.get("smdpStatus")
    active_type    = profile.get("activeType")
    data_type      = profile.get("dataType")
    activate_time  = parser.isoparse(profile["activateTime"]) if profile.get("activateTime") else None
    expired_time   = parser.isoparse(profile["expiredTime"])
    total_volume   = profile.get("totalVolume")
    total_duration = profile.get("totalDuration")
    duration_unit  = profile.get("durationUnit")
    order_usage    = profile.get("orderUsage", 0)
    esim_status    = profile.get("esimStatus")
    pin            = profile.get("pin")
    puk            = profile.get("puk")
    apn            = profile.get("apn")
    package_list   = profile.get("packageList", [])

    # 3) Upsert в БД
    existing = await EsimOrder.get_or_none(order_no=order_no, iccid=iccid)
    if existing:
        # Обновляем все поля
        existing.transaction_id = transaction_id
        existing.imsi           = imsi
        existing.msisdn         = msisdn
        existing.sms_status     = sms_status
        existing.ac             = ac
        existing.qr_code_url    = qr_code_url
        existing.short_url      = short_url
        existing.smdp_status    = smdp_status
        existing.active_type    = active_type
        existing.data_type      = data_type
        existing.activate_time  = activate_time
        existing.expired_time   = expired_time
        existing.total_volume   = total_volume
        existing.total_duration = total_duration
        existing.duration_unit  = duration_unit
        existing.order_usage    = order_usage
        existing.esim_status    = esim_status
        existing.pin            = pin
        existing.puk            = puk
        existing.apn            = apn
        existing.package_list   = package_list  # сериализуйте в JSON, если это поле не JSONField
        await existing.save()
        return existing

    # Если нет — создаём новую запись
    new_order = await EsimOrder.create(
        order_no       = order_no,
        user           = user,
        transaction_id = transaction_id,
        iccid          = iccid,
        imsi           = imsi,
        msisdn         = msisdn,
        sms_status     = sms_status,
        ac             = ac,
        qr_code_url    = qr_code_url,
        short_url      = short_url,
        smdp_status    = smdp_status,
        active_type    = active_type,
        data_type      = data_type,
        activate_time  = activate_time,
        expired_time   = expired_time,
        total_volume   = total_volume,
        total_duration = total_duration,
        duration_unit  = duration_unit,
        order_usage    = order_usage,
        esim_status    = esim_status,
        pin            = pin,
        puk            = puk,
        apn            = apn,
        package_list   = package_list,  # либо json.dumps(package_list)
    )
    return new_order