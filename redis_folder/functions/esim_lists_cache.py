from microservices import esim_lists
from redis_folder.redis_client import get_redis
import json

async def get_cache_esim_global():
    key = "esim_global"
    result = await get_redis().get(key)
    print("[DEBUG]: Redis: __get_cache_esim_global__:", result)
    return json.loads(result) if result else None

async def set_cache_esim_global():
    result = await get_redis().setex(f"esim_global", 60, json.dumps(await esim_lists.esim_global()))
    print("[DEBUG]: Redis: Cache SET: set_cache_esim_global:", result)
    return

async def get_cache():
    return

async def set_cache():
    return

async def setex_cache():
    return
