import os
from aiogram import Dispatcher, Bot, Router
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis_client import AsyncDummyRedis, init_redis_connection

bot = Bot(token=BOT_TOKEN)
router = Router()
# dp = Dispatcher(storage=MemoryStorage())
# dp.include_router(router)

# async def load_redis():
#     # Опциональное подключение Redis
#     redis = await init_redis_connection()
#     print(redis)

#     if redis is not None and hasattr(redis, "execute_command"):
#         from aiogram.fsm.storage.redis import RedisStorage
#         redis_storage = RedisStorage(redis=redis)
#         global dp
#         dp = Dispatcher(storage=redis_storage)

dp = None  # будет создан после проверки Redis

async def init_dispatcher():
    global dp

    redis = await init_redis_connection()

    if redis and not isinstance(redis, AsyncDummyRedis):
        storage = RedisStorage(redis=redis)
        print("✅ Используется RedisStorage")
    else:
        storage = MemoryStorage()
        print("🧠 Используется MemoryStorage")

    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    return dp
