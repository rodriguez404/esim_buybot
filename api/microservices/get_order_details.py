import time
import json
import hashlib

from api.http_client import get_session  # Возвращает aiohttp.ClientSession
from config import ESIM  # Должен содержать HOST_API_URL, ACCESS_CODE, SECRET_KEY

def generate_signature(body: dict, timestamp: str) -> str:
    raw = f"{ESIM.ACCESS_CODE}{json.dumps(body, separators=(',', ':'))}{timestamp}{ESIM.SECRET_KEY}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

async def get_esim_by_iccid(
    iccid: str,
    page_num: int = 1,
    page_size: int = 20,
) -> dict:
    """
    Получить один eSIM‑профиль по его ICCID.
    Если профиль найден — вернёт словарь с его данными,
    иначе — бросит LookupError.
    """
    url = f"{ESIM.HOST_API_URL}/api/v1/open/order/queryAllAllocatedProfiles"
    timestamp = str(int(time.time() * 1000))
    body = {
        "orderNo": "",    # можно оставить пустым, раз мы фильтруем по iccid
        "iccid": iccid,
        "pager": {"pageNum": page_num, "pageSize": page_size}
    }

    signature = generate_signature(body, timestamp)
    headers = {
        "RT-AccessCode": ESIM.ACCESS_CODE,
        "timestamp":      timestamp,
        "sign":           signature,
        "Content-Type":   "application/json",
    }

    client = await get_session()
    async with client.post(url, json=body, headers=headers) as resp:
        data = await resp.json()
        if resp.status != 200:
            resp.raise_for_status()
        if not data.get("success", False):
            raise Exception(f"eSIM API ошибка: {data.get('errorMsg')}")
        obj = data.get("obj", {})
        esim_list = obj.get("esimList", [])
        if not esim_list:
            raise LookupError(f"Профиль с ICCID={iccid} не найден")
        return esim_list[0]  # возвращаем первый (и обычно единственный) элемент