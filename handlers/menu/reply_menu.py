from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from localization.localization import get_text
from database.functions.get_user_lang_from_db import get_user_lang_from_db
from redis_folder.functions import get_user_lang_from_redis

async def show_reply_menu(message: types.Message, user_language: str):
    if not user_language:
        user_language = await get_user_lang_from_redis(message.from_user.id) or await get_user_lang_from_db(message.from_user.id)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text(user_language, "button.reply_menu.buy_esim")), KeyboardButton(text=get_text(user_language, "button.reply_menu.my_esim"))],
            [KeyboardButton(text=get_text(user_language, "button.reply_menu.settings")), KeyboardButton(text=get_text(user_language, "button.reply_menu.help"))],
        ],
        resize_keyboard=True,
        input_field_placeholder=get_text(user_language, "text.reply_menu.placeholder")
    )
    await message.answer(
        get_text(user_language, "text.reply_menu.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )