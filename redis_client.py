import json
from types import CoroutineType
from typing import Any, Coroutine
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
from config import REDIS
from redis.exceptions import ConnectionError
import logging

class RedisCache:
    logger = logging.getLogger(__name__)

    def __init__(self, r: Redis, prefix: str = "redis_cache:", default_ttl: int = 20):
        self.r = r
        self.prefix = prefix
        self.default_ttl = default_ttl

    def _format_key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    async def get(self, key: str, refresh_ttl: bool = False) -> Any | None:
        rkey = self._format_key(key)
        value = await self.r.get(rkey)
        if value is not None:
            if refresh_ttl:
                await self.r.expire(rkey, self.default_ttl)
            self.logger.debug(f"[CACHE HIT] {key}")
            return json.loads(value)
        self.logger.debug(f"[CACHE MISS] {key}")
        return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        data = json.dumps(value)
        await self.r.set(self._format_key(key), data, ex=ttl or self.default_ttl)
        self.logger.debug(f"[CACHE SET] {key} -> {value} (ttl={ttl or self.default_ttl})")


    async def delete(self, key: str) -> None:
        await self.r.delete(self._format_key(key))

    async def exists(self, key: str) -> bool:
        return bool(await self.r.exists(self._format_key(key)))

# Заглушка, если подключение к Redis не удалось - логирует ошибки
class AsyncDummyRedis:
    async def get(self, *args, **kwargs):
        return None

    async def set(self, *args, **kwargs):
        return False

    async def ping(self):
        return False

    def __getattr__(self, name):
        async def method(*args, **kwargs):
            print(f"Redis недоступен: попытка вызвать {name}")
            return None
        return method
    

async def get_redis_connection(host=REDIS.HOST_URL, port=6379):
    redis_client = None
    try:
        redis_client = Redis(host=host, port=port, socket_connect_timeout=2)
        # Проверяем соединение
        pong = await redis_client.ping()
        if pong:
            logging.info("✅ Успешное подключение к Redis")
        else:
            logging.warning("❌ Redis недоступен, используется заглушка")
            return AsyncDummyRedis()
        return redis_client
    except TimeoutError as err:
        logging.warning(f"⏰ Таймаут при подключении к Redis: {err}")
        return AsyncDummyRedis()
    except ConnectionError as err:
        logging.warning(f"❌ Redis недоступен, используется заглушка: {err}")
        return AsyncDummyRedis() # Возвращает заглушку, если не удалось подключиться
    except Exception as err:
        print(f"Ошибка при работе с Redis: {err}")
        return AsyncDummyRedis()


# cache = RedisCache()