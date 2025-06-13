from aiogram import Dispatcher, Bot, Router
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis_folder.redis_client import AsyncDummyRedis, init_redis_connection
from middleware.I18n_middleware import I18nMiddleware
from middleware.user_rights_middleware import UserRightsMiddleware

import logging

bot = Bot(token=BOT_TOKEN)
router = Router()

dp = None  # будет создан после проверки Redis



"""
Функция для выборки storage для Dispatcher. Если есть активный Redis - ставит RedisStorage(), иначе локальный MemoryStorage()
Storage нужен для FSM (FSMContext). В данный момент нигде не используется, но бота никак не замедляет. Добавлено для масштабируемости
Почему просто не объявить по дефолту dp = Dispatcher(storage=MemoryStorage()), 
а потом при проверке редиса перезаписать на dp = Dispatcher(storage=RedisStorage()) ?
Потому что "перезаписи" не будет. В aiogram 3.x не поддерживается изменение атрибутов существующих диспатчеров,
а новая запись dp = Dispatcher(...) создаст новый диспатчер, даже отсылаясь к глобальной переменной
"""
async def init_dispatcher():
    global dp

    redis = await init_redis_connection()

    # если вернул редис и он не является заглушкой
    if redis and not isinstance(redis, AsyncDummyRedis):
        storage = RedisStorage(redis=redis)
        logging.info("✅ Используется RedisStorage")
    # иначе - локальное хранилище
    else:
        storage = MemoryStorage()
        logging.info("🧠 Используется MemoryStorage")

    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.update.middleware(I18nMiddleware())
    dp.update.middleware(UserRightsMiddleware())
    return dp
