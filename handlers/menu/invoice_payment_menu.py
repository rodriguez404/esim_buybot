from aiogram.types import CallbackQuery, LabeledPrice
from config import PAYMENTS_TOKEN
from loader import bot


async def send_payment_invoice(callback: CallbackQuery, plan, tariff_type: str):
    if tariff_type not in ("local", "regional", "global"):
        await callback.message.answer("❌ Ошибка: тип тарифа не указан или некорректен. Обратитесь в поддержку.")
        await callback.answer()
        return

    payload = f"{tariff_type}_{plan.id}"
    print(f"[DEBUG] Тип тарифа: {tariff_type}")
    print(f"[DEBUG] Payload: {payload}")

    label_text = f"{plan.gb}ГБ • {plan.days}дней • {plan.price}$"
    rub_price = int(plan.price * 100 * 80)

    prices = [LabeledPrice(label=label_text, amount=rub_price)]

    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title="Покупка eSIM",
            description=f"Тариф: {plan.gb}ГБ на {plan.days} дней",
            payload=payload,
            provider_token=PAYMENTS_TOKEN,
            currency="RUB",
            prices=prices
        )
    except Exception as e:
        print(f"❌ Ошибка при send_invoice: {e}")
        await callback.message.answer("❌ Не удалось отправить инвойс. Попробуйте позже.")

    await callback.answer()