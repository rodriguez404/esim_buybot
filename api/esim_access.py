from .http_client import get_session
from config import ESIM

async def fetch(url: str, payload: dict, headers: dict = {'RT-AccessCode': ESIM.ACCESS_CODE}):
    session = await get_session()
    async with session.post(url, headers=headers, json=payload) as response:
        message = await response.json()
    return message
