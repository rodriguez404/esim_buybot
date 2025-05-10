"""
from aiogram import F, types
from aiogram.handlers import CallbackQueryHandler

from loader import dp
from handlers.menu import inline_menu
        
@dp.message(F.text == "🛒 Купить eSIM")
async def handle_buy(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_buy_eSIM(message)

@dp.message(F.text == "📱 Мои eSIM")
async def handle_my_esim(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_my_eSIM(message)

@dp.message(F.text == "⚙️ Настройки")
async def handle_settings(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_settings(message)

@dp.message(F.text == "📖 Помощь")
async def handle_help(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_help(message)"""

from aiogram import types, Router
from aiogram.filters import Command
from loader import dp, router
from handlers.menu import inline_menu
from localization.localization import get_text
from microservices.get_user_language import get_user_language

# Обработчик для всех кнопок reply меню с учётом языка
@router.message(~Command(commands=["start", "id"]))
async def handle_reply_menu_buttons(message: types.Message):
    user_language = await get_user_language(message.from_user.id)

    # Получаем текст всех возможных кнопок в нужном языке
    button_texts = {
        get_text(user_language, "button.replay_menu.buy_esim"): inline_menu.inline_menu_buy_eSIM,
        get_text(user_language, "button.replay_menu.my_esim"): inline_menu.inline_menu_my_eSIM,
        get_text(user_language, "button.replay_menu.settings"): inline_menu.inline_menu_settings,
        get_text(user_language, "button.replay_menu.help"): inline_menu.inline_menu_help,
    }

    action = button_texts.get(message.text)
    if action:
        try:
            await message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение пользователя: {e}")
        await action(message)
    else:
        print(f"[DEBUG] Нет действия для: {message.text}")