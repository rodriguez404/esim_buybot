def format_number(value: float):
    if value.is_integer():  # Проверяет, является ли число целым с учетом машинной точности
        return int(value)
    else:
        return value