import os
from aiogram import Dispatcher, Bot, Router
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis_folder.redis_client import AsyncDummyRedis, init_redis_connection
from middleware.I18n_middleware import I18nMiddleware

bot = Bot(token=BOT_TOKEN)
router = Router()

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
    dp.update.middleware(I18nMiddleware())
    return dp
