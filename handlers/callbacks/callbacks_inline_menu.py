from aiogram import F
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message, SuccessfulPayment, ContentType

from api.microservices.get_order_details import get_esim_details
from api.microservices.order_esim import order_esim

from database.models.esim_local import DataBase_LocalTariff
from database.models.esim_regional_and_global import DataBase_RegionalTariff
from handlers.keyboards import main_menu_kb, paginated_buttons_kb
from database.functions import esim_lists
from handlers.menu import inline_menu, invoice_payment_menu
from handlers.menu.reply_menu import show_reply_menu

from loader import bot, router

from localization.localization import get_text
from database.functions.update_user_language_in_db import update_user_language_in_db

from redis_folder.functions.get_cache_json import get_cache_json
from redis_folder.redis_client import get_redis

import logging

import json # Временно, для successful payment

@router.callback_query(F.data == "close_inline_menu")
async def close_menu_callback(callback: CallbackQuery):

    await callback.message.delete()  # Удаляет сообщение с меню


# Международные eSIM: Купить eSIM -> Международные eSIM
@router.callback_query(F.data == "global_esim_inline_menu")
async def global_esim_callback(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_global_esim(callback, user_language)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
@router.callback_query(F.data.startswith("global_plan_"))
async def selected_plan_global(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_global_esim_tariff(callback, user_language)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф -> Купить
@router.callback_query(F.data.startswith('buy_esim_global_'))
async def process_buy_esim_global(callback: CallbackQuery, user_language: str):

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_RegionalTariff.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    # Отправляем инвойс
    await invoice_payment_menu.send_payment_invoice(callback, plan)


#Региональные eSIM: Купить eSIM -> Региональные eSIM
@router.callback_query(F.data == "region_esim_inline_menu")
async def region_esim_callback(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_regional_esim(callback, user_language)


@router.callback_query(lambda c: c.data.startswith("global_page_"))
async def callback_global_page(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    plans = await get_cache_json(key="esim_global") or await esim_lists.esim_global()
    kb = paginated_buttons_kb.buttons_global_esim(plans, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("regional_page_"))
async def callback_region_page(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    plans = await get_cache_json(key=f"esim_regional_regions_{user_language}") or await esim_lists.esim_regional(user_language)
    kb = paginated_buttons_kb.buttons_region_esim(plans, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Регионы -> Клик по региону для вывода его тарифов
@router.callback_query(lambda c: c.data.startswith("region_id_"))
async def selected_region_plans(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_regional_esim_tariffs_list(callback, user_language)


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Переключение страниц по кнопкам "назад", "далее"
@router.callback_query(lambda c: c.data.startswith("regional_region_page"))
async def callback_region_page(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    region_id = int(callback.data.split("_")[-2])
    plans = await esim_lists.esim_regional_selected_region_plans(region_id)
    kb = paginated_buttons_kb.buttons_region_esim_selected(plans, region_id, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу
@router.callback_query(lambda c: c.data.startswith("regional_selected_region_plan_"))
async def selected_plan_region(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_regional_esim_tariff(callback, user_language)

# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@router.callback_query(F.data.startswith('buy_esim_regional_selected_region_'))
async def process_buy_esim_regional(callback: CallbackQuery, user_language: str):

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

    await inline_menu.inline_menu_esim_local_countries(callback, user_language)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Страны (Переключение между кнопками "назад" и "далее")
@router.callback_query(lambda c: c.data.startswith("countries_list_page_"))
async def callback_local_countries_list_page(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    countries_list = await get_cache_json(key=f"esim_local_countries_{user_language}") or await esim_lists.esim_local_countries(user_language)
    kb = paginated_buttons_kb.buttons_local_countries_esim(countries_list, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Местные eSIM: Купить eSIM -> Местные eSIM -> Страны -> Клик по стране для вывода её тарифов
@router.callback_query(lambda c: c.data.startswith("country_id_"))
async def selected_local_country_plans(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_local_esim_tariffs_list(callback, user_language)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная страна -> Все тарифы по стране -> Клик по конкретному тарифу
@router.callback_query(lambda c: c.data.startswith("selected_country_id_plan_"))
async def selected_plan_local(callback: CallbackQuery, user_language: str):

    await inline_menu.inline_menu_local_esim_tariff(callback, user_language)


# Местные eSIM: Купить eSIM -> Местные eSIM -> Конкретная Страна -> Все тарифы по стране -> Переключение страниц по кнопкам "назад", "далее"
@router.callback_query(lambda c: c.data.startswith("selected_country_plans_page_"))
async def callback_region_page(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    country_id = int(callback.data.split("_")[-2])
    plans = await esim_lists.esim_local_selected_country_plans(country_id)
    kb = paginated_buttons_kb.buttons_local_esim_selected(plans, country_id, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Конкретный Регион -> Все тарифы по региону -> Клик по конкретному тарифу -> Купить
@router.callback_query(F.data.startswith('buy_esim_selected_country_plan_'))
async def process_buy_esim_local(callback: CallbackQuery):

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

    await inline_menu.inline_menu_settings_change_language(callback, user_language)


# Настройки: Язык / Language -> RU/EN (Вполне универсальна, для дальнейшего расширения локализации добавляем только колбек в нужной форме)
@router.callback_query(F.data.in_({"change_language_ru_inline_menu", "change_language_en_inline_menu"}))
async def settings_change_language(callback: CallbackQuery, user_language: str, user_rights: str):
    lang_code = callback.data.split("_")[2]
    # current_language = await get_user_lang_from_db(callback.from_user.id)
    current_language = user_language

    if lang_code == current_language:
        await callback.answer(get_text(current_language, "notification.inline_menu.settings.change_language.already_selected"), show_alert=False)
        return

    updated = await update_user_language_in_db(callback.from_user.id, lang_code)
    user_language = lang_code if updated else current_language

    # Кэширование языка пользователя на 24 часа
    await get_redis().setex(f"user_lang:{callback.from_user.id}", 86400, lang_code)

    if updated:
        await callback.answer(
            get_text(user_language, "notification.inline_menu.settings.change_language.language_updated"), show_alert=False)
        try:
            await callback.message.delete()
        except Exception as e:
            logging.debug(f"Не удалось удалить сообщение пользователя: {e}")

        await show_reply_menu(callback.message, user_language=user_language, user_rights=user_rights)

    else:
        await callback.answer(get_text(user_language, "error.change_language"), show_alert=False)


@router.callback_query(F.data == "inline_menu_buy_esim_callback")
async def back_to_menu(callback: CallbackQuery, user_language: str):

    kb = main_menu_kb.menu_buy_esim_kb(user_language)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    amount = message.successful_payment.total_amount / 100  # Сумма в рублях
    invoice_payload = message.successful_payment.invoice_payload  # ID тарифа (payload)

    # Извлекаем информацию о тарифе
    order_plan = None
    # order_plan = await order_esim(slug=invoice_payload, user_id=message.from_user.id)
    # logging.debug(f"[SUCCESSFUL_PAYMENT: ORDER_PLAN]: {order_plan}")

    if order_plan:
        order_details = await get_esim_details(order_result=order_plan)
        logging.debug(f"[SUCCESSFUL_PAYMENT: ORDER_DETAILS]: {order_details}")
        qrcode_url = order_details.get("qrCodeUrl")
        logging.debug(f"[SUCCESSFUL_PAYMENT: QRCODE_URL]: {qrcode_url}")

        await message.answer_photo(
            photo=qrcode_url,
            caption="✅ Оплата прошла успешно!\nВаш QR-код для подключения eSIM 📲"
        )
        # await message.answer(
        #     # изменить
        #     f"✅ Оплата прошла успешно!\n"
        #     # f"Тариф: \n"
        #     # f"Сумма: {amount} {message.successful_payment.currency}\n"
        #     # f"[DEBUG] Ответ API: {json.dumps(order_plan)}\n"
        #     f"🔗 QR-код для установки: {qrcode_url}"
        # )

        # Дополнительно: выдать eSIM или пополнить баланс пользователя
        # Ваш код для активации eSIM и пополнения баланса

    else:
        await message.answer("❌ Ошибка: Тариф не найден или покупка в данный момент недоступна")


# Админка – редактировать группы тарифов - список групп
@router.callback_query(F.data == "admin_edit_tariff_groups")
async def admin_edit_tariff_groups_menu(callback: CallbackQuery, user_language: str):

    data = await esim_lists.esim_admin_tariff_groups()
    kb = paginated_buttons_kb.admin_tariff_groups_kb(data, user_language)

    await callback.message.edit_text(
        "Проверка",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Админка – редактировать группы тарифов - список групп - назад и далее
@router.callback_query(lambda c: c.data.startswith("admin_tariff_groups_page_"))
async def admin_edit_tariff_groups_menu(callback: CallbackQuery, user_language: str):

    page = int(callback.data.split("_")[-1])
    data = await esim_lists.esim_admin_tariff_groups()
    kb = paginated_buttons_kb.admin_tariff_groups_kb(data, user_language, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)


# Админка – редактировать группы тарифов - список групп - конкретная группа
@router.callback_query(lambda c: c.data.startswith("asd"))
async def admin_edit_tariff_groups_menu(callback: CallbackQuery, user_language: str):

    data = await esim_lists.esim_admin_tariff_groups()
    kb = paginated_buttons_kb.admin_tariff_groups_kb(data, user_language)

    await callback.message.edit_text(
        "Проверка",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Админка - меню (коллбек)
@router.callback_query(F.data == "menu_admin_callback")
async def menu_admin(callback: CallbackQuery, user_language: str):

    kb = main_menu_kb.menu_admin_kb(user_language)
    
    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.settings.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )

    
