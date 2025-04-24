import json
from typing import Any
from redis.asyncio import Redis

class RedisCache:
    import logging
    logger = logging.getLogger(__name__)

    def __init__(self, redis: Redis, prefix: str = "cache:", default_ttl: int = 60):
        self.redis = redis
        self.prefix = prefix
        self.default_ttl = default_ttl

    def _format_key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    async def get(self, key: str, refresh_ttl: bool = False) -> Any | None:
        rkey = self._format_key(key)
        value = await self.redis.get(rkey)
        if value is not None:
            if refresh_ttl:
                await self.redis.expire(rkey, self.default_ttl)
            self.logger.debug(f"[CACHE HIT] {key}")
            return json.loads(value)
        self.logger.debug(f"[CACHE MISS] {key}")
        return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        data = json.dumps(value)
        await self.redis.set(self._format_key(key), data, ex=ttl or self.default_ttl)
        self.logger.debug(f"[CACHE SET] {key} -> {value} (ttl={ttl or self.default_ttl})")


    async def delete(self, key: str) -> None:
        await self.redis.delete(self._format_key(key))

    async def exists(self, key: str) -> bool:
        return bool(await self.redis.exists(self._format_key(key)))
