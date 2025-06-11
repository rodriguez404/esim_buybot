import logging
import asyncio

from api.http_client import close_session

from aiogram import Bot, types
from aiogram.types import BotCommand
from aiogram.filters.command import Command

from loader import bot, init_dispatcher, router
from redis_folder.functions.set_static_cache import set_static_cache
from redis_folder.redis_client import get_redis

# Необходимы для корректной работы, несмотря на то, что визуально в мейне не используются
from handlers.menu import reply_menu, inline_menu
from handlers.callbacks import callbacks_reply_menu, callbacks_inline_menu

from tortoise.exceptions import DoesNotExist  # Правильный импорт исключения

from localization.localization import load_locales

from database import init_db
from database.models.user import DataBase_User  # Правильный импорт модели User
from database.services.user_service import get_or_create_user_db
# Обновление бд
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from microservices.update_all_packages import update_all_packages
from database.services.admin_tariff_groups_service import update_admin_tariff_groups

logging.basicConfig(level=logging.DEBUG)

# Функция настройки команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Welcome"),
        BotCommand(command="id", description="My id"),
    ]
    await bot.set_my_commands(commands)

@router.message(Command("start"))
async def cmd_start(message: types.Message, user_language: str, user_rights: str):
    await get_or_create_user_db(message.from_user)
    await reply_menu.show_reply_menu(message, user_language, user_rights)   # После регистрации или проверки, показываем главное меню

@router.message(Command("id"))
async def cmd_id(message: types.Message):
    telegram_user = message.from_user
    await message.answer(str(telegram_user.id))


async def main():
    load_locales() # Загружаем все локализации
    await init_db()

    # Планировщик - для автоматического обновления БД
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(update_all_packages, 'interval', hours=24) # Обновлять всё каждые 24 часа
    # scheduler.start()
    # print("🔁 Планировщик обновлений работает")
    
    dp = await init_dispatcher()

    await set_static_cache()
    # await update_admin_tariff_groups() # для дебаг-старта, в продакшне не нужно

    await set_commands(bot) # Устанавливаем команды для меню слева
    try:
        await dp.start_polling(bot)
    finally:
        await get_redis().close()
        await close_session()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())