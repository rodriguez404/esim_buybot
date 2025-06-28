from aiogram.types import CallbackQuery, LabeledPrice
from config import PAYMENTS_TOKEN
from loader import bot

import logging

async def send_payment_invoice(callback: CallbackQuery, plan):
    # Составляем текст для отображения
    label_text = f"{plan.gb}ГБ • {plan.days}дней • {plan.price}$"
    rub_price = int(plan.price * 100 * 80)  # конвертация: $ → копейки в рублях

    prices = [LabeledPrice(label=label_text, amount=rub_price)]
    try:
        payload = str(plan.package_code)
    except:
        payload = str(plan.slug)

    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title="Покупка eSIM",
            description=f"Тариф: {plan.gb}ГБ на {plan.days} дней.  !ВНИМАНИЕ! После успешного оформления тестового платежа будет приобретён реальный тариф",
            payload=payload,
            provider_token=PAYMENTS_TOKEN,
            currency="RUB",
            prices=prices
        )
    except Exception as e:
        logging.debug(f"❌ Ошибка при send_invoice: {e}")

    await callback.answer()  # закрывает "часики"