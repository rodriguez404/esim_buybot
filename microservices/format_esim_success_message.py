from localization.localization import get_text
def format_test_esim_issued(lang: str, plan, order) -> str:
    template = get_text(lang, "text.order.success_message")
    return template.format(
        gb=plan.gb,
        days=plan.days,
        iccid=order.iccid,
        qr_code=order.qr_code_url
    )