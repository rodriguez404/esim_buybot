from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def show_reply_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить eSIM"), KeyboardButton(text="📱 Мои eSIM")],      # Формирование столбцов и строк
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📖 Помощь")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите опцию"
    )
    await message.answer(
        """📱 *TelegramPaymentBot* — мобильный интернет-оператор *eSIM*:

    • 🌍 Покрытие в *190+ странах* (3G, 4G, 5G)  
    • ⚡ Высокая скорость  
    • 🔒 Безопасное соединение  
    • 📶 Режим модема  
    • 💸 Самые низкие цены


    Выберите подходящее для Вас направление и тариф и пользуйтесь мобильным интернетом *через минуту после оплаты*.

    *eSIM от TelegramPaymentBot* можно использовать одновременно с Вашей *основной SIM-картой*.

    ➡️ Перейдите в меню _«Купить eSIM»_ или воспользуйтесь поиском ниже.  
    ⚙️ Изменить способ оплаты можно в меню _«Настройки»_.
    """,
        reply_markup=kb,
        parse_mode="Markdown"
    )
    # Если хочешь использовать HTML-форматирование вместо Markdown (например, <b>жирный</b>, <i>курсив</i>), просто укажи parse_mode="HTML".(ограничения ~4096 символов на сообщение)