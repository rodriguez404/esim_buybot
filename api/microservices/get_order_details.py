from api.http_client import get_session
from api.microservices.generate_signature import generate_signature
from config import ESIM
import time
import logging

async def get_esim_details(
    order_result: dict,
    page_num: int = 1,
    page_size: int = 20,
) -> dict:
    
    order_obj = order_result.get("obj", {})
    logging.debug(f"[GET_ESIM_DETAILS: ORDER_OBJ]: {order_obj}")
    esimList = order_obj.get("esimList", [{}])[0]
    logging.debug(f"[GET_ESIM_DETAILS: ESIMLIST]: {esimList}")
    orderNo = esimList.get("orderNo")
    logging.debug(f"[GET_ESIM_DETAILS: ORDER_NO]: {orderNo}")

    """
    Получить заказ по его orderNo.
    Если профиль найден — вернёт словарь с его данными,
    иначе — бросит LookupError.
    """
    url = f"{ESIM.HOST_API_URL}//api/v1/open/esim/query"
    timestamp = str(int(time.time() * 1000))
    body = {
        "orderNo": orderNo,
        "esimTranNo": "",
        "iccid": "",
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
            raise LookupError(f"Профиль с OrderNo={orderNo} не найден")
        return esim_list[0]  # возвращаем первый (и обычно единственный) элемент
