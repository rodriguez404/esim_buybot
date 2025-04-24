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

    await inline_menu.inline_menu_help(message)