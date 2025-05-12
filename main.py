import logging
import asyncio

from api.http_client import close_session

from aiogram import Bot, types
from aiogram.types import BotCommand
from aiogram.filters.command import Command

from loader import bot, init_dispatcher
from redis_folder.functions.esim_lists_cache import set_cache_esim_global
from redis_folder.redis_client import get_redis

from handlers.menu import reply_menu, inline_menu
from handlers.callbacks import callbacks_reply_menu, callbacks_inline_menu

from tortoise.exceptions import DoesNotExist  # Правильный импорт исключения

from localization.localization import load_locales

from database import init_db
from database.models.user import DataBase_User  # Правильный импорт модели User
from database.services.user_service import get_or_create_user_db
from database.services.esim_service_global import update_esim_packages_global
from database.services.esim_service_regional import update_esim_packages_regional
from database.services.esim_service_local import update_esim_packages_local

from loader import router
from redis_folder.redis_client import get_redis

logging.basicConfig(level=logging.DEBUG)

# Функция настройки команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Welcome"),
        BotCommand(command="id", description="My id"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("start"))
async def cmd_start(message: types.Message, user_language: str):
    await get_or_create_user_db(message.from_user)
    await reply_menu.show_reply_menu(message, user_language)   # После регистрации или проверки, показываем главное меню

@router.message(Command("id"))
async def cmd_id(message: types.Message):
    telegram_user = message.from_user
    await message.answer(str(telegram_user.id))


async def main():
    load_locales() # Загружаем все локализации

    await init_db()
    # await update_esim_packages_global()
    # await update_esim_packages_regional()
    # await update_esim_packages_local()
    dp = await init_dispatcher()

    await set_cache_esim_global() # временно?, для отладки

    await set_commands(bot) # Устанавливаем команды для меню слева
    try:
        await dp.start_polling(bot)
    finally:
        await get_redis().close()
        await close_session()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())