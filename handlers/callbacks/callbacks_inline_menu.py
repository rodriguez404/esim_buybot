from aiogram import F, types

from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.types import PreCheckoutQuery, Message

from database.models.esim_global import DataBase_EsimPackageGlobal
from handlers.keyboards.buttons_menu import buttons_region_esim, buttons_global_esim, buttons_region_esim_selected
from handlers.menu.esim_lists import esim_global, esim_regional, esim_regional_selected
from handlers.menu import inline_menu, invoice_payment_menu

from loader import dp, bot
from config import PAYMENTS_TOKEN

@dp.callback_query(F.data == "close_inline_menu")
async def close_menu_callback(callback: CallbackQuery):
    await callback.message.delete()  # Удаляет сообщение с меню


# Международные eSIM: Купить eSIM -> Международные eSIM
@dp.callback_query(F.data == "global_esim_inline_menu")
async def global_esim_callback(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_global_esim(callback.message)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф
@dp.callback_query(F.data.startswith("global_plan_"))
async def selected_plan_global(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_global_esim_tariff(callback)


# Международные тарифы eSIM: Купить eSIM -> Международные eSIM -> Конкретный тариф -> Купить
@dp.callback_query(F.data.startswith('buy_esim_global_'))
async def process_buy_esim(callback: CallbackQuery):
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
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")

    await inline_menu.inline_menu_regional_esim(callback.message)


@dp.callback_query(lambda c: c.data.startswith("global_page_"))
async def callback_global_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    plans = await esim_global()
    kb = buttons_global_esim(plans, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("regional_page_"))
async def callback_region_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    plans = await esim_regional()
    kb = buttons_region_esim(plans, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("regional_region_"))
async def callback_region_page(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[-1])
    region_id = int(callback.data.split("_")[-3])
    plans = await esim_regional_selected(region_id)
    kb = buttons_region_esim_selected(plans, region_id, page=page)

    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("region_id_"))
async def selected_plan_region(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение пользователя: {e}")
    await inline_menu.inline_menu_regional_esim_tariff(callback)


# Обработчик на кнопки Назад-Вперед для всех менюшек
# @dp.callback_query(F.data.startswith("page_"))
# async def process_pagination(callback: CallbackQuery):
#     page = int(callback.data.split("_")[1])
#     kb = paginate_buttons(data, page=page)
#     await callback.message.edit_reply_markup(reply_markup=kb)
#     await callback.answer()

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

