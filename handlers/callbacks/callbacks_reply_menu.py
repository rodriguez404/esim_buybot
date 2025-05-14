from aiogram import types
from aiogram.filters import Command
from database.functions.get_user_lang_from_db import get_user_lang_from_db
from loader import router
from handlers.menu import inline_menu
from localization.localization import get_text
from redis_folder.functions import get_user_lang_from_redis

# Обработчик для всех кнопок reply меню с учётом языка
@router.message(~Command(commands=["start", "id"]))
async def handle_reply_menu_buttons(message: types.Message):
    user_language = await get_user_lang_from_redis(message.from_user.id) or await get_user_lang_from_db(message.from_user.id)
    # Получаем текст всех возможных кнопок в нужном языке
    button_texts = {
        get_text(user_language, "button.reply_menu.buy_esim"): inline_menu.inline_menu_buy_eSIM,
        get_text(user_language, "button.reply_menu.my_esim"): inline_menu.inline_menu_my_eSIM,
        get_text(user_language, "button.reply_menu.settings"): inline_menu.inline_menu_settings,
        get_text(user_language, "button.reply_menu.help"): inline_menu.inline_menu_help,
    }

    action = button_texts.get(message.text)
    if action:
        try:
            await message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение пользователя: {e}")
        await action(message, user_language)
    else:
        print(f"[DEBUG] Нет действия для: {message.text}")