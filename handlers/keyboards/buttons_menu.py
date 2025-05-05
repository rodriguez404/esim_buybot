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

# Региональные eSIM: Регион -> Тарифы конкретного региона
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

# Местные eSIM: Купить eSIM -> Местные eSIM (список стран)
def buttons_local_countries_esim(countries_list: list[list[int]], page: int = 0, buttons_per_page: int = 16) -> InlineKeyboardMarkup:

    # Для избежания цикличного импорта - ленивый вариант, т.к. используется только в одной функции,
    # Если будут нужны флаги в нескольких функциях, лучше переделать
    from handlers.menu.inline_menu import code_to_flag 

    total_pages = (len(countries_list) + buttons_per_page - 1) // buttons_per_page

    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    current_page_data = countries_list[start:end]

    keyboard = []

    # Формируем кнопки стран в 2 столбца
    for i in range(0, len(current_page_data), 2):  # Шаг 2 для двух кнопок в строке
        row = []
        # Добавляем первую кнопку в строку
        if i < len(current_page_data):
            country_id, country_name, country_code = current_page_data[i]
            row.append(InlineKeyboardButton(
                text=f"{code_to_flag(country_code)}{country_name}",
                callback_data=f"country_id_{country_id}"
            ))
        # Добавляем вторую кнопку в строку (если есть)
        if i + 1 < len(current_page_data):
            country_id, country_name, country_code = current_page_data[i + 1]
            row.append(InlineKeyboardButton(
                text=f"{code_to_flag(country_code)}{country_name}", 
                callback_data=f"country_id_{country_id}"
            ))
        keyboard.append(row)

    # Навигация по страницам в 2 столбца, если есть
    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"countries_list_page_{page - 1}"))
    if end < len(countries_list):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"countries_list_page_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Добавляем нижние кнопки
    keyboard.append([
        InlineKeyboardButton(text="Меню", callback_data="inline_menu_buy_eSIM"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
    ])


    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Местные eSIM: Страна -> Тарифы конкретной страны
def buttons_local_esim_selected(plans: list[list[int]], country_id: int, page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:

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
        callback_data = f"selected_country_id_plan_{country_id}_{plan_id}"
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    # Навигация по страницам в 2 столбца, если есть
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"selected_country_id_page_{country_id}_{page - 1}"))
    if end < len(plans):
        navigation_buttons.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"selected_country_id_page_{country_id}_{page + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    # Добавляем нижние кнопки
    keyboard.append([
        InlineKeyboardButton(text="Меню", callback_data="local_esim_inline_menu"),
        InlineKeyboardButton(text="Закрыть", callback_data="close_inline_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)