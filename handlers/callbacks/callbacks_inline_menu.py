from aiogram import F, types

from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.types import PreCheckoutQuery, Message

from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_local import DataBase_LocalTariff
from database.models.esim_regional import DataBase_RegionalTariff
from handlers.keyboards.buttons_menu import buttons_region_esim, buttons_global_esim, buttons_region_esim_selected, buttons_local_countries_esim, buttons_local_esim_selected
from handlers.menu.esim_lists import esim_global, esim_regional, esim_regional_selected_region_plans, esim_local_countries, esim_local_selected_country_plans
from handlers.menu import inline_menu, invoice_payment_menu

from loader import dp, bot
from config import PAYMENTS_TOKEN

@dp.callback_query(F.data == "close_inline_menu")
async def close_menu_callback(callback: CallbackQuery):
    await callback.message.delete()  # Удаляет сообщение с меню


# Международные eSIM: Купить eSIM -> Международные eSIM
@dp.callback_query(F.data == "global_esim_inline_menu")
async def global_esim_callback(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_global_esim(callback.message)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
@dp.callback_query(F.data.startswith("global_plan_"))
async def selected_plan_global(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_global_esim_tariff(callback)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф -> Купить
@dp.callback_query(F.data.startswith('buy_esim_global_'))
async def process_buy_esim_global(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_EsimPackageGlobal.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer("⚠️ Ошибка: тариф не найден.")
        return

    # Отправляем инвойс
    await invoice_payment_menu.send_payment_invoice(callback, plan)


# Региональные eSIM: Купить eSIM -> Региональные eSIM
@dp.callback_query(F.data == "region_esim_inline_menu")
async def region_esim_callback(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_regional_esim(callback.message)


@dp.callback_query(lambda c: c.data.startswith("global_page_"))
async def callback_global_page(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    page = int(callback.data.split("_")[-1])
    plans = await esim_global()
    kb = buttons_global_esim(plans, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("regional_page_"))
async def callback_region_page(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    page = int(callback.data.split("_")[-1])
    plans = await esim_regional()
    kb = buttons_region_esim(plans, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Регионы -> Клик по региону для вывода его тарифов
@dp.callback_query(lambda c: c.data.startswith("region_id_"))
async def selected_plan_region(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_regional_esim_tariffs_list(callback)


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Переключение страниц по кнопкам "назад", "далее"
@dp.callback_query(lambda c: c.data.startswith("regional_region_page"))
async def callback_region_page(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    page = int(callback.data.split("_")[-1])
    region_id = int(callback.data.split("_")[-2])
    plans = await esim_regional_selected_region_plans(region_id)
    kb = buttons_region_esim_selected(plans, region_id, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу
@dp.callback_query(lambda c: c.data.startswith("regional_selected_region_plan_"))
async def selected_plan_region(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_regional_esim_tariff(callback)

# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@dp.callback_query(F.data.startswith('buy_esim_regional_selected_region_'))
async def process_buy_esim_regional(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_RegionalTariff.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer("⚠️ Ошибка: тариф не найден.")
        return

    # Отправляем инвойс
    await invoice_payment_menu.send_payment_invoice(callback, plan)

# Местные eSIM: Купить eSIM -> Местные eSIM
@dp.callback_query(F.data == "local_esim_inline_menu")
async def local_countries_esim_callback(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_esim_local_countries(callback.message)

# Местные eSIM: Купить eSIM -> Местные eSIM -> Страны (Переключение между кнопками "назад" и "далее")
@dp.callback_query(lambda c: c.data.startswith("countries_list_page_"))
async def callback_local_countries_list_page(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    page = int(callback.data.split("_")[-1])
    countries_list = await esim_local_countries()
    kb = buttons_local_countries_esim(countries_list, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Местные eSIM: Купить eSIM -> Местне eSIM -> Страны -> Клик по стране для вывода её тарифов
@dp.callback_query(lambda c: c.data.startswith("country_id_"))
async def selected_plan_region(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_local_esim_tariffs_list(callback)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная страна -> Все тарифы по стране -> Клик по конкретному тарифу
@dp.callback_query(lambda c: c.data.startswith("selected_country_id_plan_"))
async def selected_plan_local(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_local_esim_tariff(callback)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная Страна -> Все тарифы по стране -> Переключение страниц по кнопкам "назад", "далее"
@dp.callback_query(lambda c: c.data.startswith("selected_country_id_page_"))
async def callback_region_page(callback: types.CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #
    page = int(callback.data.split("_")[-1])
    country_id = int(callback.data.split("_")[-2])
    plans = await esim_local_selected_country_plans(country_id)
    kb = buttons_local_esim_selected(plans, country_id, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@dp.callback_query(F.data.startswith('buy_esim_selected_country_plan_'))
async def process_buy_esim_local(callback: CallbackQuery):
    # Временно - для отладки
    # При клике на кнопку выводит в консоль её callback.data айдишник
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    #

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_LocalTariff.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer("⚠️ Ошибка: тариф не найден.")
        return
    
    await invoice_payment_menu.send_payment_invoice(callback, plan)

# Настройки -> Язык / Language
@dp.callback_query(F.data == "choose_language")
async def language_list(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    from aiogram.types import InlineKeyboardButton
    kb = [
        InlineKeyboardButton(text="Русский", callback_data="language_ru"),
        InlineKeyboardButton(text="English", callback_data="language_en")
    ]

    text = (
        f"\n*🌍 Пожалуйста, выберите Язык:*\n"
        "Please, select a Language:"
    )

    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query(F.data.startswith("language_"))
async def choose_language_click(callback: CallbackQuery):

    from redis_cache import set_user_language

    lang = str(callback.data.split("_")[-1])
    user_id = CallbackQuery.from_user.id
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    set_user_language(user_id, lang)

    text = {
        "ru": "Ваш язык успешно сохранён.",
        "en": "Language saved successfuly."
    }

    await callback.message.answer(text[lang], parse_mode="Markdown")

# ТЕСТОВЫЙ МУСОР ДЛЯ ПЛАТЕЖКИ
@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data
    if data == "inline_menu_buy_eSIM":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM(callback.message)
    elif data == "inline_menu_global_esim":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM_ru(callback.message)
    elif data == "btn1":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM_ru(callback.message)

    await callback.answer()

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    amount = message.successful_payment.total_amount / 100  # Сумма в рублях
    invoice_payload = message.successful_payment.invoice_payload  # ID тарифа (payload)

    # Извлекаем информацию о тарифе
    plan_id = int(invoice_payload.split("_")[-1])  # Извлекаем ID тарифа из payload
    plan = await DataBase_EsimPackageGlobal.get_or_none(id=plan_id)

    if plan:
        await message.answer(
            f"✅ Оплата прошла!\n"
            f"Тариф: {plan.name}\n"
            f"Сумма: {amount} {message.successful_payment.currency}\n"
            "Тариф активирован! Все необходимые данные для активации eSIM отправлены на ваш телефон."
        )

        # Дополнительно: выдать eSIM или пополнить баланс пользователя
        # Ваш код для активации eSIM и пополнения баланса

    else:
        await message.answer("❌ Ошибка: Тариф не найден.")


# Временно - для отладки
# Для всех незарегистрированных хэндлерами выше кнопок
# При клике на кнопку выводит в консоль её callback.data айдишник
@dp.callback_query()
async def handle_callback_debug(callback: CallbackQuery):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    await callback.answer()