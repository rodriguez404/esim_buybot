# Функция для получения флага по коду страны (например, "US" -> 🇺🇸)
def code_to_flag(code: str) -> str:
    return "".join(chr(127397 + ord(c.upper())) for c in code)