import os
from aiogram import Dispatcher, Bot, Router
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from redis_client import AsyncDummyRedis, get_redis_connection

bot = Bot(token=BOT_TOKEN)
router = Router()
memory_storage = MemoryStorage()
dp = Dispatcher(storage=memory_storage)
dp.include_router(router)

# Опциональное подключение Redis
async def try_load_redis():
    redis_client = await get_redis_connection()
    if not isinstance(redis_client, AsyncDummyRedis): # Подключаем Redis-хранилище для dp, если получили Не заглушку
        from aiogram.fsm.storage.redis import RedisStorage
        redis_storage = RedisStorage(redis=redis_client)
        global dp
        dp = Dispatcher(storage=redis_storage)