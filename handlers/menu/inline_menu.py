import re

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from handlers.menu import esim_lists

from handlers.keyboards.buttons_menu import buttons_global_esim, buttons_region_esim, buttons_region_esim_selected
from database.models.esim_global import DataBase_EsimCountryGlobal, DataBase_EsimPackageGlobal
from database.models.esim_regional import DataBase_RegionalTariff


#Купить eSIM
async def inline_menu_buy_eSIM(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔥 Популярные направления", callback_data="btn1")],
            [InlineKeyboardButton(text="Местная eSIM", callback_data="country_esim_inline_menu")],
            [InlineKeyboardButton(text="Региональная eSIM", callback_data="region_esim_inline_menu")],
            [InlineKeyboardButton(text="Международная eSIM", callback_data="global_esim_inline_menu")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await message.answer(
        "*Купить eSIM*\n"
        "Вы можете купить eSIM как для отдельной страны, так и для определенного региона:",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Международные eSIM: Купить eSIM -> Международные eSIM
async def inline_menu_global_esim(message: types.Message):
    data = await esim_lists.esim_global()
    kb = buttons_global_esim(data, page=0)
    await message.answer(
        "*🌍 Международные eSIM-пакеты:*\n"
        "Пожалуйста, выберите необходимый объем интернет-трафика:",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
async def inline_menu_global_esim_tariff(callback: CallbackQuery):
    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_EsimPackageGlobal.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer("⚠️ Ошибка: тариф не найден.")
        return

    # Получаем список стран с кодами
    countries = await DataBase_EsimCountryGlobal.filter(package_id=plan.id).values("location_name", "location_code")
    countries_text = ", ".join(f"{code_to_flag(c['location_code'])} {c['location_name']}" for c in countries) \
        if countries else "страны не найдены"

    # Клавиатура
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Купить eSIM • {plan.price}$", callback_data=f"buy_esim_global_{plan.id}")],
            [
                InlineKeyboardButton(text="Назад", callback_data="global_esim_inline_menu"),
                InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
            ]
        ]
    )

    # Основной текст
    text = (
        "*🌍 Международная eSIM*\n"
        f"Вы выбрали eSIM с тарифом *{plan.gb} ГБ на {plan.days} дней*. В тариф также входит:\n"
        "   • Неограниченная скорость;\n"
        "   • Безопасное соединение;\n"
        "   • Режим модема.\n\n"
        f"🗺️ eSIM будет работать в следующих странах: {countries_text}\n\n"
        "⚠️ На eSIM доступен только интернет-трафик, который работает в указанных странах. "
        "Для оформления eSIM не требуется удостоверение личности.\n\n"
        "После оплаты Вы получите QR-код и дополнительную информацию для установки eSIM. "
        "Срок действия eSIM отсчитывается с момента ее активации на Вашем устройстве.\n\n"
        "---------\n\n"
        "Перед покупкой eSIM, пожалуйста, убедитесь, что Ваше устройство поддерживается "
        "(iOS (https://t.me/fedafone_bot/ios_ru), Android (https://t.me/fedafone_bot/android_ru), "
        "Windows (https://t.me/fedafone_bot/windows_ru)).\n\n"
        "Нажимая кнопку Купить eSIM Вы соглашаетесь с условиями и положениями "
        "(https://t.me/fedafone_bot/terms_ru).\n\n"
        "💳 Изменить способ оплаты можно в меню Настройки."
    )

    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

# Региональные eSIM: Купить eSIM -> Региональные eSIM
async def inline_menu_regional_esim(message: types.Message):
    data = await esim_lists.esim_regional()
    kb = buttons_region_esim(data, page=0)
    await message.answer(
        "*🌍 Региональные eSIM-пакеты:*\n"
        "Пожалуйста, выберите регион, где Вам нужен мобильный интернет:",
        reply_markup=kb,
        parse_mode="Markdown"
    )

# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Все тарифы конкретного региона
async def inline_menu_regional_esim_tariff(callback: CallbackQuery):
    region_id = int(callback.data.split("_")[-1])

    # Получаем тарифы по ID

    plans = await esim_lists.esim_regional_selected(region_id=region_id)
    print("~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("region_id: ", region_id)
    print("plans: ", plans)
    kb = buttons_region_esim_selected(plans, region_id=region_id, page=0)

    # Основной текст
    text = (
        "*🌍 Региональные тарифы:*\n"
    )

    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

#Мои eSIM
async def inline_menu_my_eSIM(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Купить eSIM", callback_data="btn1")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await message.answer(
        "*Мои eSIM*\n"
        "У Вас пока нет ни одной eSIM. Хотите купить eSIM?",
        reply_markup=kb,
        parse_mode="Markdown"
    )

#Настройки
async def inline_menu_settings(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Способы оплаты ⇨", callback_data="btn1")],
            [InlineKeyboardButton(text="Язык / Language ⇨", callback_data="btn2")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await message.answer(
        "*Настройки*\n"
        "Пожалуйста, выберите необходимый пункт:",
        reply_markup=kb,
        parse_mode="Markdown"
    )

#Помощь
async def inline_menu_help(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Справочный центр", callback_data="btn1")],
            [InlineKeyboardButton(text="IOS", callback_data="btn2"), InlineKeyboardButton(text="Android", callback_data="btn3"), InlineKeyboardButton(text="Windows", callback_data="btn4")],
            [InlineKeyboardButton(text="Веб-сайт telegram-payment-bot", callback_data="btn3")],
            [InlineKeyboardButton(text="Приложение telegram-payment-bot для iPhone", callback_data="btn3")],
            [InlineKeyboardButton(text="Реферальная программа", callback_data="btn3")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await message.answer(
        "*Помощь*\n"
        "Вы можете обратиться напрямую в техническую поддержку @telegramPaymentBotSupport или выбрать нужный раздел:",
        reply_markup=kb,
        parse_mode="Markdown"
    )

#Тестовая покупка
async def inline_menu_buy_eSIM_ru(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 ГБ на 7 дней -> 5$", callback_data="tariff_ru_1")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await message.answer(
        "*🇷🇺 Россия*\n"
        "Пожалуйста, выберите необходимый объем интернет-трафика:",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Функция для получения флага по коду страны (например, "US" -> 🇺🇸) НЕ УДАЛЯТЬ БЛЯТЬ, ПОТОМ САМ ПЕРЕМЕЩУ!
def code_to_flag(code: str) -> str:
    return "".join(chr(127397 + ord(c.upper())) for c in code)





