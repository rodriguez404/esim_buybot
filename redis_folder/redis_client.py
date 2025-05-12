from redis.asyncio import Redis
from config import REDIS
from redis.exceptions import ConnectionError
import logging
from redis_folder.redis_mock_class import AsyncDummyRedis
    
# Попытка подключения к серверу. Возвращает заглушку, если не удалось
redis_client: Redis | None = None
redis_is_working: bool = False
async def init_redis_connection(host=REDIS.HOST_URL, port=6379):
    global redis_client
    try:
        redis_client = Redis(host=host, port=port, decode_responses=True, socket_connect_timeout=3)
        # Проверяем соединение
        pong = await redis_client.ping()
        if pong:
            logging.info("✅ Успешное подключение к Redis")
            global redis_is_working
            redis_is_working = True # Для функции get_redis()
        else:
            logging.warning("❌ Redis недоступен, используется заглушка")
            return AsyncDummyRedis() # Возвращает заглушку, если не удалось подключиться
        return redis_client # Возвращает рабочий клиент Redis
    except TimeoutError as err:
        logging.warning(f"⏰ Таймаут при подключении к Redis: {err}")
        return AsyncDummyRedis() # Возвращает заглушку, если не удалось подключиться
    except ConnectionError as err:
        logging.warning(f"❌ Redis недоступен, используется заглушка: {err}")
        return AsyncDummyRedis() # Возвращает заглушку, если не удалось подключиться
    except Exception as err:
        print(f"Ошибка при работе с Redis: {err}")
        return AsyncDummyRedis()

# Повсеместная функция для обращения к редису
def get_redis():
    if (redis_is_working):
        return redis_client
    else:
        return AsyncDummyRedis()
