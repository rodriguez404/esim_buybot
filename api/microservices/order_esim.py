import hashlib
import time
import json
import uuid

from api.http_client import get_session  # Возвращает aiohttp.ClientSession
from config import ESIM  # Должен содержать HOST_API_URL, ACCESS_CODE, SECRET_KEY


def generate_signature(body: dict, timestamp: str) -> str:
    raw = f"{ESIM.ACCESS_CODE}{json.dumps(body, separators=(',', ':'))}{timestamp}{ESIM.SECRET_KEY}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


async def order_esim(slug: str, price: float, count: int = 1) -> dict:
    url = f"{ESIM.HOST_API_URL}/api/v1/open/esim/order"
    timestamp = str(int(time.time() * 1000))

    price_api = int(price * 10000)
    total_amount = price_api * count

    body = {
        "transactionId": str(uuid.uuid4()),
        "amount": total_amount,
        "packageInfoList": [
            {
                "packageCode": slug,
                "count": count,
                "price": price_api
            }
        ]
    }

    signature = generate_signature(body, timestamp)

    headers = {
        "RT-AccessCode": ESIM.ACCESS_CODE,
        "timestamp": timestamp,
        "sign": signature,
        "Content-Type": "application/json"
    }

    print(f"[DEBUG] POST URL: {url}")
    print(f"[DEBUG] BODY: {body}")
    print(f"[DEBUG] HEADERS: {headers}")

    client = await get_session()

    async with client.post(url, json=body, headers=headers) as response:
        data = await response.json()

        if not response.status == 200:
            print(f"[DEBUG] RESPONSE DATA (HTTP error): {data}")
            response.raise_for_status()

        # Проверка по success/кодам
        if not data.get("success"):
            print(f"[DEBUG] RESPONSE DATA (error): {data}")
            message = data.get("errorMsg", "Неизвестная ошибка")
            raise Exception(f"eSIM API ошибка: {message}")

        if not data.get("obj"):
            raise Exception("eSIM API вернул пустой результат")

        return data["obj"]