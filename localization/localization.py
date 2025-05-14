import json
from pathlib import Path

# Переменная для хранения локалей
_locales = {}
LOCALES_DIR = Path("localization/locales")

def load_locales():
    """Загружает все локализации в память"""
    global _locales
    for path in LOCALES_DIR.glob("*.json"):
        lang = path.stem  # Извлекаем название языка из имени файла (например, ru или en)
        with path.open(encoding="utf-8") as f:
            _locales[lang] = json.load(f)

def get_text(lang: str, key: str) -> str:
    """Получает текст по ключу для конкретного языка"""
    return _locales.get(lang, {}).get(key, f"[{key}]")  # Возвращает текст или сам ключ, если не найдено

"""def translate_countries(key: str, lang: str) -> str:
    return _locales.get(lang, {}).get("countries", {}).get(key, f"[{key}]")"""


def translate_countries(key: str, lang: str) -> str:
    translation = _locales.get(lang, {}).get("countries", {}).get(key, f"[{key}]")

    # Проверяем, если страна не найдена, выводим в консоль
    if translation == f"[{key}]":
        print(f"Не удалось найти перевод для страны: {key} на языке {lang}")

    return translation


def translate_regions(key: str, lang: str) -> str:
    translation = _locales.get(lang, {}).get("regions", {}).get(key, f"[{key}]")

    # Проверяем, если страна не найдена, выводим в консоль
    if translation == f"[{key}]":
        print(f"Не удалось найти перевод для страны: {key} на языке {lang}")

    return translation