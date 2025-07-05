import time
from datetime import datetime, timezone

import logging
from api.esim_access import fetch
from config import ESIM

import json
from api.microservices.generate_signature import generate_signature

# Для проверки цены
from database.models.esim_local import DataBase_LocalTariff
from database.models.esim_regional_and_global import DataBase_RegionalTariff
from database.models.user_transactions import DataBase_UserTransactions


async def order_esim(slug: str, user_id: int, count: int = 1):
    url = f"{ESIM.HOST_API_URL}/api/v1/open/esim/order"
    timestamp_default = time.time()
    timestamp_miliseconds = timestamp_default * 1000
    timestamp_str = str(int(timestamp_miliseconds))

    # объявляется отдельно для package_info["price"] в body
    regional_pkg_price = await DataBase_RegionalTariff.get_or_none(slug=slug)
    local_pkg_price = await DataBase_LocalTariff.get_or_none(slug=slug)
    price_obj = regional_pkg_price or local_pkg_price

    package_info = {
        "packageCode": slug,
        "count": count,
        "price": 10000 * price_obj.price
    }

    body = {
        "transactionId": f"{user_id}_{timestamp_str}_{slug}", # уникальные ID транзакций: айдиПользователя_времяПокупки_слаг
        "amount": package_info["price"] * count,
        "packageInfoList": [package_info]
    }

    signature = generate_signature(body, timestamp_str)

    headers = {
        "RT-AccessCode": ESIM.ACCESS_CODE,
        "timestamp": timestamp_str,
        "sign": signature,
        "Content-Type": "application/json"
    }

    try:
        order_result = await fetch(url=url, payload=body, headers=headers)
        logging.debug(json.dumps(order_result))
    except Exception as e:
        logging.error(f"[ORDER_ESIM] Ошибка при создании запроса: {e}", exc_info=True)

    if order_result:
        try:
            DataBase_UserTransactions.create(
                user_id=user_id,
                slug=slug,
                count=count,
                date=datetime.fromtimestamp(timestamp_default, tz=timezone.utc),
                orderNo=order_result.get("obj", {}).get("esimList", [{}])[0].get("orderNo"),
                transactionId=order_result.get("obj", {}).get("esimList", [{}])[0].get("transactionId")
            )
        except Exception as e:
            logging.error(f"[ORDER_ESIM] Ошибка при записи в базу данных: {e}", exc_info=True)

    return order_result