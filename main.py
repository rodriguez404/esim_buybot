import logging
import asyncio

from redis import Redis
from api.http_client import close_session

import config
from aiogram import Bot, types, Router, Dispatcher
from aiogram.types import BotCommand
from aiogram.filters.command import Command

from loader import dp, bot, try_load_redis

from handlers.menu import reply_menu, inline_menu
from handlers.callbacks import callbacks_reply_menu, callbacks_inline_menu

from tortoise.exceptions import DoesNotExist  # Правильный импорт исключения

from localization.localization import load_locales

from database import init_db
from database.models.user import DataBase_User  # Правильный импорт модели User
from database.services.user_service import get_or_create_user
from database.services.esim_service_global import update_esim_packages_global
from database.services.esim_service_regional import update_esim_packages_regional
from database.services.esim_service_local import update_esim_packages_local

# Успех

logging.basicConfig(level=logging.DEBUG)

# Функция настройки команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Welcome"),
        BotCommand(command="id", description="My id"),
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await get_or_create_user(message.from_user)
    await reply_menu.show_reply_menu(message)   # После регистрации или проверки, показываем главное меню

@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    telegram_user = message.from_user
    await message.answer(str(telegram_user.id))


async def main():
    # Опциональное подключение Redis
    redis_client = await try_load_redis()

    load_locales() # Загружаем все локализации

    await init_db()
    # await update_esim_packages_global()
    # await update_esim_packages_regional()
    # await update_esim_packages_local()
    await set_commands(bot) # Устанавливаем команды для меню слева
    try:
        await dp.start_polling(bot)
    finally:
        await redis_client.close()
        await close_session()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())