from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.functions import esim_lists

from handlers.keyboards import main_menu_kb, paginated_buttons_kb
from database.models.esim_global import DataBase_EsimPackageGlobal
from database.models.esim_regional import DataBase_RegionalTariff
from database.models.esim_local import DataBase_LocalTariff

from localization.localization import get_text
from database.functions.get_user_lang_from_db import get_user_lang_from_db
from microservices.format_number_UI import format_number
from redis_folder.functions import get_user_lang_from_redis
from redis_folder.functions.get_cache_json import get_cache_json



# Местные eSIM: Купить eSIM -> Местные eSIM
async def inline_menu_esim_local_countries(callback: CallbackQuery, user_language: str):

    data = await get_cache_json(key=f"esim_local_countries_{user_language}") or await esim_lists.esim_local_countries(user_language)
    kb = paginated_buttons_kb.buttons_local_countries_esim(data, user_language, page=0)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.local_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Местные eSIM: Купить eSIM -> Местные eSIM -> Все тарифы конкретной страны
async def inline_menu_local_esim_tariffs_list(callback: CallbackQuery, user_language: str):

    country_id = int(callback.data.split("_")[-1])  # Получаем тарифы по ID региона

    plans = await esim_lists.esim_local_selected_country_plans(country_id=country_id)
    kb = paginated_buttons_kb.buttons_local_esim_selected(plans, country_id=country_id, user_language=user_language, page=0)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.local_esim.all_tariffs.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Местные eSIM: Купить eSIM -> Местные eSIM -> Все тарифы конкретной страны -> Конкретный тариф
async def inline_menu_local_esim_tariff(callback: CallbackQuery, user_language: str):

    plan_id = int(callback.data.split("_")[-1])
    country_id = int(callback.data.split("_")[-2])

    # Получаем тариф по ID
    plan = await DataBase_LocalTariff.get_or_none(id=plan_id, country_id=country_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    # Клавиатура
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.local_esim.all_tariffs.current_tariff").format(price=format_number(plan.price)), callback_data=f"buy_esim_selected_country_plan_{country_id}_{plan.id}")],
            [
                InlineKeyboardButton(text=get_text(user_language, "button.back"), callback_data=f"selected_country_plans_page_{country_id}_0"),
                InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")
            ]
        ]
    )

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.local_esim.all_tariffs.current_tariff.text_menu").format(gb=format_number(plan.gb), days=plan.days),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Региональные eSIM: Купить eSIM -> Региональные eSIM
async def inline_menu_regional_esim(callback: CallbackQuery, user_language: str):

    data = await get_cache_json(key=f"esim_regional_regions_{user_language}") or await esim_lists.esim_regional(user_language)
    kb = paginated_buttons_kb.buttons_region_esim(data, user_language, page=0)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.regional_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Все тарифы конкретного региона
async def inline_menu_regional_esim_tariffs_list(callback: CallbackQuery, user_language: str):

    region_id = int(callback.data.split("_")[-1])

    # Получаем тарифы по ID региона
    plans = await esim_lists.esim_regional_selected_region_plans(region_id=region_id)
    kb = paginated_buttons_kb.buttons_region_esim_selected(plans, region_id=region_id, user_language=user_language, page=0)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.regional_esim.all_tariffs.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Все тарифы конкретного региона -> Конкретный тариф
async def inline_menu_regional_esim_tariff(callback: CallbackQuery, user_language: str):

    plan_id = int(callback.data.split("_")[-1])
    region_id = int(callback.data.split("_")[-2])

    # Получаем тариф по ID
    plan = await DataBase_RegionalTariff.get_or_none(id=plan_id, region=region_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    countries_text = await esim_lists.esim_regional_countries(plan_id, region_id, user_language)
    if not countries_text:
        countries_text = get_text(user_language, "error.countries_not_found")

    # Клавиатура
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.regional_esim.all_tariffs.current_tariff").format(price=format_number(plan.price)), callback_data=f"buy_esim_regional_selected_region_{region_id}_{plan.id}")],
            [
                InlineKeyboardButton(text=get_text(user_language, "button.back"), callback_data=f"regional_region_page_{region_id}_0"),
                InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")
            ]
        ]
    )

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.regional_esim.all_tariffs.current_tariff.text_menu").format(gb=format_number(plan.gb), days=plan.days, countries=countries_text),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Международные eSIM: Купить eSIM -> Международные eSIM
async def inline_menu_global_esim(callback: CallbackQuery, user_language: str):

    data = await get_cache_json(key="esim_global") or await esim_lists.esim_global()
    kb = paginated_buttons_kb.buttons_global_esim(data, user_language, page=0)

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.global_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
async def inline_menu_global_esim_tariff(callback: CallbackQuery, user_language: str):

    plan_id = int(callback.data.split("_")[-1])

    # Получаем тариф по ID
    plan = await DataBase_EsimPackageGlobal.get_or_none(id=plan_id)
    if not plan:
        await callback.message.answer(get_text(user_language, "error.tariff_not_found"))
        return

    countries_text = await esim_lists.esim_global_countries(plan.id, user_language)
    if not countries_text:
        countries_text = get_text(user_language, "error.countries_not_found")

    # Клавиатура
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.global_esim.current_tariff").format(price=format_number(plan.price)), callback_data=f"buy_esim_global_{plan.id}")],
            [
                InlineKeyboardButton(text=get_text(user_language, "button.back"), callback_data="global_esim_inline_menu"),
                InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")
            ]
        ]
    )

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.buy_esim.global_esim.current_tariff.text_menu").format(gb=format_number(plan.gb), days=plan.days, countries=countries_text),
        reply_markup=kb,
        parse_mode="Markdown"
    )

# Для доступа из нажатия реплай кнопки. Выдаёт новое сообщение
async def replyPress_menu_buy_esim(message: types.Message, user_language: str):

    kb = main_menu_kb.menu_buy_esim_kb(user_language)

    await message.answer(
        get_text(user_language, "text.inline_menu.buy_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


#Мои eSIM
async def replyPress_menu_my_esim(message: types.Message, user_language: str):

    kb = main_menu_kb.menu_my_esim_kb(user_language)

    await message.answer(
        get_text(user_language, "text.inline_menu.my_esim.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Настройки (по нажатию в реплай клавиатуре, отправляет новое сообщение)
async def replyPress_menu_settings(message: types.Message, user_language: str):

    kb = main_menu_kb.menu_settings_kb(user_language)

    await message.answer(
        get_text(user_language, "text.inline_menu.settings.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Настройки (по нажатию из инлайн клавиатуры, редактирует текущее сообщение)
async def inline_menu_settings_callback(callback: CallbackQuery, user_language: str):

    kb = main_menu_kb.menu_settings_kb(user_language)

    await callback.message.answer(
        get_text(user_language, "text.inline_menu.settings.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


# Админка (по нажатию в реплай клавиатуре, отправляет новое сообщение)
async def replyPress_menu_admin(message: types.Message, user_language: str):

    kb = main_menu_kb.menu_admin_kb(user_language)

    await message.answer(
        get_text(user_language, "text.inline_menu.settings.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


async def inline_menu_settings_change_language(callback: CallbackQuery, user_language: str):
    user_language = await get_user_lang_from_redis(callback.from_user.id) or await get_user_lang_from_db(callback.from_user.id)
    
    lang_ru_text = get_text(user_language, "button.inline_menu.settings.change_language.ru")
    lang_en_text = get_text(user_language, "button.inline_menu.settings.change_language.en")

    # "✅" к выбранному языку
    if user_language == "ru":
        lang_ru_text = f"✅ {lang_ru_text}"
    elif user_language == "en":
        lang_en_text = f"✅ {lang_en_text}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=lang_ru_text, callback_data="change_language_ru_inline_menu"),
                InlineKeyboardButton(text=lang_en_text, callback_data="change_language_en_inline_menu")
            ],
            [
                InlineKeyboardButton(text=get_text(user_language, "button.menu"), callback_data="inline_menu_settings_callback"),
                InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")
            ]
        ]
    )

    await callback.message.edit_text(
        get_text(user_language, "text.inline_menu.settings.change_language.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


#Помощь
async def replyPress_menu_help(message: types.Message, user_language: str):

    kb = main_menu_kb.menu_help_kb(user_language)

    await message.answer(
        get_text(user_language, "text.inline_menu.help.text_menu"),
        reply_markup=kb,
        parse_mode="Markdown"
    )


#Тестовая покупка ("Популярные направления")
async def inline_menu_buy_eSIM_ru(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 ГБ на 7 дней -> 5$", callback_data="tariff_ru_1")],
            [InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")]
        ]
    )

    await callback.message.edit_text(
        "*🇷🇺 Россия*\n"
        "Пожалуйста, выберите необходимый объем интернет-трафика:",
        reply_markup=kb,
        parse_mode="Markdown"
    )