from types import NoneType
from database.models.user import DataBase_User
from redis_client import get_redis, AsyncDummyRedis
import logging


async def get_user_language(user_id: int) -> str:
    redis = get_redis()
    # Сначала проверяем кэш Redis
    print(redis)
    print("Тип клиента Redis:", type(redis))
    if redis is not NoneType and redis is not None and redis is not isinstance(redis, AsyncDummyRedis):
        lang_bytes = await redis.get(f"user_lang:{user_id}")
        if lang_bytes:
            lang = lang_bytes.decode('utf-8')
            logging.debug(f"[Redis] Найден язык для пользователя {user_id}: {lang}")
            return lang
        else:
            logging.debug(f"[Redis] CACHE MISS for user_lang:{user_id}")
    else:
        logging.debug("Redis не работает. Переход к БД")

    user = await DataBase_User.filter(id=user_id).first()
    if user:
        return user.language
    return "ru"