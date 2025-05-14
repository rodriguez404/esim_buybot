import json
import logging

from redis_folder.redis_client import get_redis
from redis_folder.redis_mock_class import AsyncDummyRedis

# Обертка для дефолтного redis.get(), которая сразу обрабатывает json
async def get_cache_json(key):
    if isinstance(get_redis(), AsyncDummyRedis()):
        return None
    
    result = await get_redis().get(key)
    logging.debug(f"[DEBUG]: Redis: __get_cache_json_{key}__:", result)
    return json.loads(result) if result else None