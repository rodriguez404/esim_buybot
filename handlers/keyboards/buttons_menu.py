from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from localization.localization import get_text
from microservices.format_number_UI import format_number

# Универсальная функция для генерации инлайн-клавиатуры с пагинацией
def generate_paginated_kb(
    data: list,
    user_language: str,
    pagination_prefix: str,
    page: int = 0,
    buttons_per_page: int = 8,
    columns: int = 1,
    menu_callback: str = "inline_menu_buy_eSIM_callback",
    button_formatter=None,
) -> InlineKeyboardMarkup:
    """
    :data: Парсинг данных для отображения (с редиса или бд)
    :user_language: Язык пользователя
    :page: Текущая страница (по дефолту 0)
    :buttons_per_page: Количество кнопок на странице (по дефолту 8)
    :columns: Количество столбцов (1 или 2, по дефолту 1)
    :menu_callback: Коллбэк для возврата в меню (по дефолту возвращает на главную, но меняется для возврата в меню местных, меню регионов и тд)
    :button_formatter: Функция, формирующая одну кнопку (страна, тариф страны, регион, тариф региона и тд)
    """

    total_pages = (len(data) + buttons_per_page - 1) // buttons_per_page
    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    current_page_data = data[start:end]

    keyboard = []

    # Формируем кнопки в нужное количество столбцов
    for i in range(0, len(current_page_data), columns):
        row = []
        for j in range(columns):
            index = i + j
            if index < len(current_page_data):
                row.append(button_formatter(current_page_data[index], user_language))
        if row:
            keyboard.append(row)

    # Навигационные кнопки (назад и далее)
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text=get_text(user_language, "button.back"),
            callback_data=f"{pagination_prefix}_{page - 1}"
        ))
    if end < len(data):
        navigation_buttons.append(InlineKeyboardButton(
            text=get_text(user_language, "button.next"),
            callback_data=f"{pagination_prefix}_{page + 1}"
        ))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Дополнительные кнопки (меню и закрыть)
    keyboard.append([
        InlineKeyboardButton(text=get_text(user_language, "button.menu"), callback_data=menu_callback),
        InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Форматирование кнопки страны
def format_country_button(item, user_language):
    country_id, country_name, country_flag = item
    return InlineKeyboardButton(text=f"{country_flag}{country_name}",callback_data=f"country_id_{country_id}")


# Форматирование кнопки региона
def format_region_button(item, user_language):
    region_id, region_name = item
    return InlineKeyboardButton(text=f"{region_name}",callback_data=f"region_id_{region_id}")


# Форматирование кнопки тарифа (под страны)
def format_country_plan_button(country_id):
    def formatter(item, user_language):
        plan_id, gb, days, price = item
        text = get_text(user_language, "button.keyboards.buy_esim.local_esim.all_tariffs.current_tariff").format(gb=format_number(gb), days=days, price=format_number(price))
        callback_data = f"selected_country_id_plan_{country_id}_{plan_id}"
        return InlineKeyboardButton(text=text, callback_data=callback_data)
    return formatter


# Форматирование кнопки тарифа (под регионы)
def format_region_plan_button(region_id):
    def formatter(item, user_language):
        plan_id, gb, days, price = item
        text = get_text(user_language, "button.keyboards.buy_esim.local_esim.all_tariffs.current_tariff").format(gb=format_number(gb), days=days, price=format_number(price))
        callback_data = f"regional_selected_region_plan_{region_id}_{plan_id}"
        return InlineKeyboardButton(text=text, callback_data=callback_data)
    return formatter


# Форматирование кнопки тарифа (под глобалы)
def format_global_plan_button(item, user_language):
    plan_id, gb, days, price = item
    text = get_text(user_language, "button.keyboards.buy_esim.global_esim").format(gb=format_number(gb), days=days, price=format_number(price))
    callback_data = f"global_plan_{plan_id}"
    return InlineKeyboardButton(text=text, callback_data=callback_data)


# Местные eSIM: Купить eSIM -> Местные eSIM (список стран)
def buttons_local_countries_esim(countries_list, user_language: str, page=0):
    return generate_paginated_kb(
        data=countries_list,
        user_language=user_language,
        page=page,
        buttons_per_page=16,
        columns=2,
        button_formatter=format_country_button,
        pagination_prefix="countries_list_page"
    )


# Местные eSIM: Купить eSIM -> Местные eSIM (список стран) -> Тарифы конкретной страны
def buttons_local_esim_selected(plans: list[list[int]], country_id: int, user_language: str, page: int = 0) -> InlineKeyboardMarkup:
    return generate_paginated_kb(
        data=plans,
        user_language=user_language,
        page=page,
        buttons_per_page=8,
        columns=1,
        button_formatter=format_country_plan_button(country_id),
        pagination_prefix=f"selected_country_plans_page_{country_id}",
        menu_callback="local_esim_inline_menu"
    )


# Региональные eSIM: Купить eSIM -> Региональные eSIM
def buttons_region_esim(plans: list[list[int]], user_language: str, page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:
    return generate_paginated_kb(
        data=plans,
        user_language=user_language,
        page=page,
        buttons_per_page=8,
        columns=1,
        button_formatter=format_region_button,
        pagination_prefix="regional_page",
    )


# Региональные eSIM: Купить eSIM -> Региональные eSIM -> Все тарифы конкретного региона
def buttons_region_esim_selected(plans: list[list[int]], region_id: int, user_language: str, page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:
    return generate_paginated_kb(
        data=plans,
        user_language=user_language,
        page=page,
        buttons_per_page=8,
        columns=1,
        button_formatter=format_region_plan_button(region_id),
        pagination_prefix=f"regional_region_page_{region_id}",
        menu_callback="region_esim_inline_menu"
    )


# Международные eSIM: Купить eSIM -> Международные eSIM
def buttons_global_esim(plans: list[list[int]], user_language: str, page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:
    return generate_paginated_kb(
        data=plans,
        user_language=user_language,
        page=page,
        buttons_per_page=8,
        columns=1,
        button_formatter=format_global_plan_button,
        pagination_prefix=f"global_page",
    )
