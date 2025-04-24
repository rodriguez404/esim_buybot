from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Международные eSIM
def buttons_global_esim(plans: list[list[int]], page: int = 0, buttons_per_page: int = 8) -> InlineKeyboardMarkup:
    """
    :param plans: список тарифов в формате [id, gb, days, price]
    :param page: текущая страница
    :param buttons_per_page: количество кнопок на страницу
    :return: InlineKeyboardMarkup с пагинацией
    """
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



def paginate_buttons_region(data, page=0, buttons_per_page=15):
    total_pages = (len(data) + buttons_per_page - 1) // buttons_per_page
    page = max(0, min(page, total_pages - 1))

    start = page * buttons_per_page
    end = start + buttons_per_page
    page_data = data[start:end]

    # Создаем по 2 кнопки в ряд
    rows = []
    for i in range(0, len(page_data), 2):
        row = []
        for item in page_data[i:i+2]:
            name = item
            text = f"{name}"
            callback = f"select_region_{name.replace(' ', '_')}"  # или другой идентификатор
            row.append(InlineKeyboardButton(text=text, callback_data=callback))
        rows.append(row)

    # Кнопки "Назад/Далее"
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page-1}"))
    if end < len(data):
        nav.append(InlineKeyboardButton(text="➡️ Далее", callback_data=f"page_{page+1}"))
    if nav:
        rows.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=rows)