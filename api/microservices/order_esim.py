import hashlib
import hmac
import uuid
import time
import json
from datetime import datetime, timezone

import logging
from api.esim_access import fetch
from config import ESIM

# Для проверки цены
from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_local import DataBase_LocalTariff
from database.models.esim_regional import DataBase_RegionalTariff
from database.models.user_transactions import DataBase_UserTransactions
from microservices.get_user_id import get_user_id

secretKey_bytes = ESIM.SECRET_KEY.encode('utf-8') # Кодирует строку в байтовое представление

def generate_signature(request_body: dict, timestamp: str = str(int(time.time() * 1000))) -> str:
    request_id = str(uuid.uuid4())
    request_body = json.dumps(request_body, separators=(',', ':'), sort_keys=True)
    signData: str = timestamp + request_id + ESIM.ACCESS_CODE + request_body
    signData_bytes = signData.encode('utf-8')
    signature = hmac.new(secretKey_bytes, signData_bytes, hashlib.sha256).hexdigest().lower()
    logging.debug(f"[GENERATE_SIGNATURE]\nTimestamp={timestamp}\nRequestID={request_id}\nAccessCode={ESIM.ACCESS_CODE}\nSecretKey={ESIM.SECRET_KEY}\nRequestBody={request_body}\nsignStr={signData}\nSignature={signature}")
    return signature


async def order_esim(package_code: str, user_id: int, count: int = 1):
    # url = f"{ESIM.HOST_API_URL}/esim-order-api/v2/order"
    url = f"{ESIM.HOST_API_URL}/api/v1/open/esim/order"
    timestamp = str(int(time.time() * 1000))

    # объявляется отдельно для package_info["price"] в body
    global_pkg_price = await DataBase_EsimPackageGlobal.get_or_none(package_code=package_code)
    regional_pkg_price = await DataBase_RegionalTariff.get_or_none(package_code=package_code)
    local_pkg_price = await DataBase_LocalTariff.get_or_none(package_code=package_code)
    price_obj = global_pkg_price or regional_pkg_price or local_pkg_price

    package_info = {
        "packageCode": package_code,
        "count": count,
        "price": 10000 * price_obj.price
    }

    body = {
        "transactionId": f"{timestamp}_{user_id}_{package_code}", # Сам придумал, уникальные айди транзакций: время_айдиПользователя_кодПакета
        "amount": package_info["price"] * count,
        "packageInfoList": [package_info]
    }

    signature = generate_signature(body, timestamp)

    headers = {
        "RT-AccessCode": ESIM.ACCESS_CODE,
        "timestamp": timestamp,
        "sign": signature,
        "Content-Type": "application/json"
    }

    try:
        order_result = await fetch(url=url, payload=body, headers=headers)
    except Exception as e:
        logging.debug(f"[ORDER_ESIM] Ошибка при создании запроса: {e}")

    if order_result:
        try:
            DataBase_UserTransactions.create(
                user_id=user_id,
                package_code=package_code,
                count=count,
                date=datetime.fromtimestamp(timestamp, tz=timezone.utc),
                orderNo=order_result['obj']['orderNo'],
                transactionId=order_result['obj']['transactionId']
            )
        except Exception as e:
            logging.debug(f"[ORDER_ESIM] Ошибка при записи в базу данных: {e}")

    return order_result