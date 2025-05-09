import os
from aiogram import Dispatcher, Bot, Router
from config import REDIS, BOT_TOKEN
from redis.asyncio import Redis
from redis_cache import *
from aiogram.fsm.storage.redis import RedisStorage

bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher(storage=redis_storage) #dp = Dispatcher()
dp.include_router(router)