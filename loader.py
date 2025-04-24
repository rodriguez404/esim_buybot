import os
from aiogram import Dispatcher, Bot, Router
from config import REDIS, BOT_TOKEN
from redis.asyncio import Redis
from redis_cache import RedisCache
from aiogram.fsm.storage.redis import RedisStorage

redis = Redis(host=os.getenv(REDIS.HOST_URL), port=os.getenv(REDIS.PORT), decode_responses=True)
cache = RedisCache(redis, prefix="tg:", default_ttl=60)
redis_storage = RedisStorage(redis)

bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher(storage=redis_storage) #dp = Dispatcher()
dp.include_router(router)