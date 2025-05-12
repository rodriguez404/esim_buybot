from aiogram import F, types, Router

from aiogram.types import CallbackQuery
from aiogram.types import PreCheckoutQuery, Message

from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_local import DataBase_LocalTariff
from database.models.esim_regional import DataBase_RegionalTariff
from handlers.keyboards import buttons_menu
from microservices import esim_lists
from handlers.menu import inline_menu, invoice_payment_menu
from handlers.menu.reply_menu import show_reply_menu

from loader import bot, router

from localization.localization import get_text
from database.functions.get_user_lang_from_db import get_user_lang_from_db
from microservices.update_user_language import update_user_language_in_db

from redis_folder.redis_client import get_redis

@router.callback_query(F.data == "close_inline_menu")
async def close_menu_callback(callback: CallbackQuery):
    await callback.message.delete()  # Удаляет сообщение с меню


# Международные eSIM: Купить eSIM -> Международные eSIM
@router.callback_query(F.data == "global_esim_inline_menu")
async def global_esim_callback(callback: CallbackQuery, user_language: str):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_global_esim(callback, user_language)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
@router.callback_query(F.data.startswith("global_plan_"))
async def selected_plan_global(callback: CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_global_esim_tariff(callback, user_language)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф -> Купить
@router.callback_query(F.data.startswith('buy_esim_global_'))
async def process_buy_esim_global(callback: CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)
    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_EsimPackageGlobal.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    # Отправляем инвойс
    await invoice_payment_menu.send_payment_invoice(callback, plan)


# Региональные eSIM: Купить eSIM -> Региональные eSIM
@router.callback_query(F.data == "region_esim_inline_menu")
async def region_esim_callback(callback: CallbackQuery, user_language: str):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_regional_esim(callback, user_language)


@router.callback_query(lambda c: c.data.startswith("global_page_"))
async def callback_global_page(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    page = int(callback.data.split("_")[-1])
    plans = await esim_lists.esim_global()
    kb = buttons_menu.buttons_global_esim(plans, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("regional_page_"))
async def callback_region_page(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    page = int(callback.data.split("_")[-1])
    plans = await esim_lists.esim_regional(user_language)
    kb = buttons_menu.buttons_region_esim(plans, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Регионы -> Клик по региону для вывода его тарифов
@router.callback_query(lambda c: c.data.startswith("region_id_"))
async def selected_plan_region(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_regional_esim_tariffs_list(callback, user_language)


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Переключение страниц по кнопкам "назад", "далее"
@router.callback_query(lambda c: c.data.startswith("regional_region_page"))
async def callback_region_page(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    page = int(callback.data.split("_")[-1])
    region_id = int(callback.data.split("_")[-2])
    plans = await esim_lists.esim_regional_selected_region_plans(region_id)
    kb = buttons_menu.buttons_region_esim_selected(plans, region_id, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу
@router.callback_query(lambda c: c.data.startswith("regional_selected_region_plan_"))
async def selected_plan_region(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_regional_esim_tariff(callback, user_language)

# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@router.callback_query(F.data.startswith('buy_esim_regional_selected_region_'))
async def process_buy_esim_regional(callback: CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_RegionalTariff.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    # Отправляем инвойс
    await invoice_payment_menu.send_payment_invoice(callback, plan)

# Местные eSIM: Купить eSIM -> Местные eSIM
@router.callback_query(F.data == "local_esim_inline_menu")
async def local_countries_esim_callback(callback: CallbackQuery, user_language: str):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_esim_local_countries(callback, user_language)

# Местные eSIM: Купить eSIM -> Местные eSIM -> Страны (Переключение между кнопками "назад" и "далее")
@router.callback_query(lambda c: c.data.startswith("countries_list_page_"))
async def callback_local_countries_list_page(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    page = int(callback.data.split("_")[-1])
    countries_list = await esim_lists.esim_local_countries(user_language)
    kb = buttons_menu.buttons_local_countries_esim(countries_list, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Местные eSIM: Купить eSIM -> Местне eSIM -> Страны -> Клик по стране для вывода её тарифов
@router.callback_query(lambda c: c.data.startswith("country_id_"))
async def selected_plan_region(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_local_esim_tariffs_list(callback, user_language)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная страна -> Все тарифы по стране -> Клик по конкретному тарифу
@router.callback_query(lambda c: c.data.startswith("selected_country_id_plan_"))
async def selected_plan_local(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_local_esim_tariff(callback, user_language)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная Страна -> Все тарифы по стране -> Переключение страниц по кнопкам "назад", "далее"
@router.callback_query(lambda c: c.data.startswith("selected_country_id_page_"))
async def callback_region_page(callback: types.CallbackQuery, user_language: str):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    page = int(callback.data.split("_")[-1])
    country_id = int(callback.data.split("_")[-2])
    plans = await esim_lists.esim_local_selected_country_plans(country_id)
    kb = buttons_menu.buttons_local_esim_selected(plans, country_id, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@router.callback_query(F.data.startswith('buy_esim_selected_country_plan_'))
async def process_buy_esim_local(callback: CallbackQuery):

    # Временно для отладки - выводит в консоль callback.data айдишник
    print("[DEBUG] Button pressed: ", callback.data)

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_LocalTariff.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer("⚠️ Ошибка: тариф не найден.")
        return
    
    await invoice_payment_menu.send_payment_invoice(callback, plan)

# Настройки: Язык / Language
@router.callback_query(F.data == "change_language_inline_menu")
async def settings_change_language(callback: CallbackQuery, user_language: str):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_settings_change_language(callback, user_language)


# Настройки: Язык / Language -> RU/EN (Вполне универсальна, для дальнейшего расширения локализации добавляем только колбек в нужной форме)
@router.callback_query(F.data.in_({"change_language_ru_inline_menu", "change_language_en_inline_menu"}))
async def settings_change_language(callback: CallbackQuery, user_language: str):
    lang_code = callback.data.split("_")[2]
    # current_language = await get_user_lang_from_db(callback.from_user.id)
    current_language = user_language

    if lang_code == current_language:
        await callback.answer(get_text(current_language, "notification.inline_menu.settings.change_language.already_selected"), show_alert=False)
        return

    updated = await update_user_language_in_db(callback.from_user.id, lang_code)
    user_language = lang_code if updated else current_language

    redis = get_redis()
    await redis.set(f"user_lang:{callback.from_user.id}", lang_code)
    # Debug - временно - для отладки
    print(f"Тип Redis клиента: {type(redis)}")
    #

    if updated:
        await callback.answer(
            get_text(user_language, "notification.inline_menu.settings.change_language.language_updated"), show_alert=False)
        try:
            await callback.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение пользователя: {e}")

        await show_reply_menu(callback.message, user_language=user_language)

    else:
        await callback.answer(get_text(user_language, "error.change_language"), show_alert=False)


# ТЕСТОВЫЙ МУСОР ДЛЯ ПЛАТЕЖКИ(НЕ МУСОР, Я ПЕРЕДУМАЛ) 
# - МУСОР, ПЕРЕДЕЛАЕШЬ @rodriguez404 to 4EJlOBEK06
@router.callback_query()
async def handle_callback(callback: CallbackQuery, user_language: str):
    data = callback.data
    if data == "inline_menu_buy_eSIM_callback":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM_callback(callback, user_language)
    if data == "inline_menu_settings_callback":
        await callback.message.delete()
        await inline_menu.inline_menu_settings_callback(callback, user_language)
    elif data == "inline_menu_global_esim":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM_ru(callback)
    elif data == "btn1":
        await callback.message.delete()
        await inline_menu.inline_menu_buy_eSIM_ru(callback)

    await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
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
@router.callback_query()
async def handle_callback_debug(callback: CallbackQuery):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DEBUG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("button pressed: ", callback.data)
    await callback.answer()