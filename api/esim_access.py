from .http_client import get_session
from config import ESIM

host = ESIM.HOST_API_URL
url_packagelist = ESIM.API_PACKAGELIST_URL
url_locationlist = ESIM.API_PACKAGELIST_URL

async def fetch(url, payload):
    session = await get_session()
    headers = {'RT-AccessCode': {ESIM.ACCESS_CODE}}
    async with session.post(url, headers=headers, json=payload) as response:
        message: dict = await response.json()
    return message
