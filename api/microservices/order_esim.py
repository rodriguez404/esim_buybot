import hashlib
import time
import json

from http_client import get_session
from config import ESIM
from esim_access import fetch


def generate_signature(body: dict, timestamp: str) -> str:
    raw = f"{ESIM.ACCESS_CODE}{json.dumps(body, separators=(',', ':'))}{timestamp}{ESIM.SECRET_KEY}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

async def order_esim(package_code: str, count: int = 1):
    url = f"{ESIM.HOST_API_URL}/esim-order-api/v2/order"
    timestamp = str(int(time.time() * 1000))

    body = {
        "packageCode": package_code,
        "count": count
    }

    signature = generate_signature(body, timestamp)

    headers = {
        "accessCode": ESIM.ACCESS_CODE,
        "timestamp": timestamp,
        "sign": signature,
        "Content-Type": "application/json"
    }

    async with get_session() as client:
        response = await client.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()