from aiogram import types
from aiogram.filters import Command
from config import ADMINS
from loader import router
from handlers.menu import inline_menu
from localization.localization import get_text

# Обработчик для всех кнопок reply меню с учётом языка
@router.message(~Command(commands=["start", "id"]))
async def handle_reply_menu_buttons(message: types.Message, user_language: str):
    # Получаем текст всех возможных кнопок в нужном языке
    button_texts = {
        get_text(user_language, "button.reply_menu.buy_esim"): inline_menu.replyPress_menu_buy_esim,
        get_text(user_language, "button.reply_menu.my_esim"): inline_menu.replyPress_menu_my_esim,
        get_text(user_language, "button.reply_menu.settings"): inline_menu.replyPress_menu_settings,
        get_text(user_language, "button.reply_menu.help"): inline_menu.replyPress_menu_help,
        get_text(user_language, "button.reply_menu.admin"): inline_menu.replyPress_menu_admin,
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