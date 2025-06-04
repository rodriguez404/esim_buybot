from database.functions.get_user_lang_from_db import get_user_lang_from_db
from redis_folder.redis_client import get_redis, AsyncDummyRedis
import logging

async def get_user_lang_from_redis(user_id: int) -> str:
    redis = get_redis()
    if redis and not isinstance(redis, AsyncDummyRedis): # "Если не заглушка" - ...
        lang = await redis.get(f"user_lang:{user_id}")
        if lang:
            # lang_decoded = lang_bytes.decode('utf-8') # Используем, если в Redis-клиенте флаг decode_responses стоит False
            logging.debug(f"[Redis] Найден язык для пользователя {user_id}: {lang}")
            return lang
        else:
            logging.debug(f"[Redis] CACHE MISS for user_lang:{user_id}. Запись кэша")
            await redis.setex(f"user_lang:{user_id}", 86400, get_user_lang_from_db)

    else:
        logging.debug("[Redis] Redis не работает. Переход к БД")