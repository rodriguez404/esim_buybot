import os
from aiogram import Dispatcher, Bot, Router
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from redis_client import AsyncDummyRedis, init_redis_connection
# from redis_client import redis_client

bot = Bot(token=BOT_TOKEN)
router = Router()
memory_storage = MemoryStorage()
dp = Dispatcher(storage=memory_storage)
dp.include_router(router)

# Опциональное подключение Redis
async def try_load_redis():
    global redis_client
    redis_client = await init_redis_connection()
    print("Тип клиента Redis:", type(redis_client))
    if not isinstance(redis_client, AsyncDummyRedis): # Подключаем Redis-хранилище для dp, если получили Не заглушку
        from aiogram.fsm.storage.redis import RedisStorage
        redis_storage = RedisStorage(redis=redis_client)
        global dp
        dp = Dispatcher(storage=redis_storage)