from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from localization.localization import get_text


def menu_buy_esim_kb(user_language: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            # [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.popular_destinations"), callback_data="btn1")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.local_esim"), callback_data="local_esim_inline_menu")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.buy_esim.regional_and_global_esim"), callback_data="region_esim_inline_menu")],
            [InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")]
        ]
    )
    return kb


def menu_my_esim_kb(user_language: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")]
        ]
    )
    return kb


def menu_settings_kb(user_language: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            # [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.settings.payment_methods"), callback_data="btn1")], # Способы оплаты
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.settings.change_language"), callback_data="change_language_inline_menu")],
            [InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")]
        ]
    )
    return kb


def menu_help_kb(user_language: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.help_center"), callback_data="btn1")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.ios"), callback_data="btn2"), InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.android"), callback_data="btn3"), InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.windows"), callback_data="btn4")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.website"), callback_data="btn3")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.application_for_ios"), callback_data="btn3")],
            [InlineKeyboardButton(text=get_text(user_language, "button.inline_menu.help.referral_program"), callback_data="btn3")],
            [InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")]
        ]
    )
    return kb


def menu_admin_kb(user_language: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Редактировать группы тарифов", callback_data="admin_edit_tariff_groups")],
            [InlineKeyboardButton(text=get_text(user_language, "button.close"), callback_data="close_inline_menu")]
        ]
    )
    return kb