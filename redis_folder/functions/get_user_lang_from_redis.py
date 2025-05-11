from redis_folder.redis_client import get_redis, AsyncDummyRedis
import logging

async def get_user_lang_from_redis(user_id: int) -> str:
    redis = get_redis()
    # Сначала проверяем кэш Redis
    if redis is not isinstance(redis, AsyncDummyRedis):
        lang_bytes = await redis.get(f"user_lang:{user_id}")
        if lang_bytes:
            lang = lang_bytes.decode('utf-8')
            logging.debug(f"[Redis] Найден язык для пользователя {user_id}: {lang}")
            return lang
        else:
            logging.debug(f"[Redis] CACHE MISS for user_lang:{user_id}")
    else:
        logging.debug("Redis не работает. Переход к БД")