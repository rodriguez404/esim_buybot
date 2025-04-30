from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Международные eSIM
def buttons_global_esim(plans: list[list[int]], page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:

    total_pages = (len(plans) + buttons_per_page - 1) // buttons_per_page
    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    current_page_data = plans[start:end]

    keyboard = []

    # Формируем один столбец для тарифов
    for plan in current_page_data:
        plan_id, gb, days, price = plan
        text = f"{gb} ГБ на {days} дней — {price}$"
        callback_data = f"global_plan_{plan_id}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    # Навигация по страницам в 2 столбца, если есть
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"global_page_{page - 1}"))
    if end < len(plans):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"global_page_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Добавляем нижние кнопки
    keyboard.append([
        InlineKeyboardButton(text="Меню", callback_data="inline_menu_buy_eSIM"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def buttons_region_esim(plans: list[list[int]], page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:
    total_pages = (len(plans) + buttons_per_page - 1) // buttons_per_page

    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    current_page_data = plans[start:end]

    keyboard = []

    # Формируем один столбец для регионов
    for plan in current_page_data:
        region_id, region_name = plan
        text = f"{region_name}"
        callback_data = f"region_id_{region_id}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    # Навигация по страницам в 2 столбца, если есть
    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"regional_page_{page - 1}"))
    if end < len(plans):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"regional_page_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Добавляем нижние кнопки
    keyboard.append([
        InlineKeyboardButton(text="Меню", callback_data="inline_menu_buy_eSIM"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
    ])


    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Международные eSIM
def buttons_region_esim_selected(plans: list[list[int]], region_id: int, page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:

    total_pages = (len(plans) + buttons_per_page - 1) // buttons_per_page
    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    current_page_data = plans[start:end]

    keyboard = []

    # Формируем один столбец для тарифов
    for plan in current_page_data:
        plan_id, gb, days, price = plan
        text = f"{gb} ГБ на {days} дней — {price}$"
        callback_data = f"regional_selected_region_plan_{region_id}_{plan_id}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    # Навигация по страницам в 2 столбца, если есть
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"regional_region_page_{region_id}_{page - 1}"))
    if end < len(plans):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"regional_region_page_{region_id}_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Добавляем нижние кнопки
    keyboard.append([
        InlineKeyboardButton(text="Меню", callback_data="region_esim_inline_menu"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)