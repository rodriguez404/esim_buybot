'''
Форматирование одной кнопки
Для клавиатур с пагинацией
'''

from aiogram.types import InlineKeyboardButton

from localization.localization import get_text
from microservices.format_number_UI import format_number

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


# Форматирование кнопки группы тарифов (админка)
def format_admin_tariff_group_button(item, user_language):
    group_id, group_countries, group_prices, group_name = item
    text = group_name
    callback_data = f"admin_tariff_group_{group_id}"
    return InlineKeyboardButton(text=text, callback_data=callback_data)