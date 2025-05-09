from redis_cache import r
from . import en, ru
# from database import get_user_language_from_db

LANG_MODULES = {
    "en": en,
    "ru": ru,
}

DEFAULT_LANGUAGE = "ru"

# def get_user_language_from_db(user_id: int) -> str:
#     return

def get_language(user_id: int) -> str:
    lang = r.get(f"user:{user_id}:lang")
    if lang:
        return lang.decode("utf-8")
    
    # lang_from_db = get_user_language_from_db(user_id)
    # if lang_from_db:
    #     r.set(f"user:{user_id}:lang", lang_from_db)  # кэшируем в Redis
    #     return lang_from_db

    return DEFAULT_LANGUAGE

def text_with_user_lang(user_id: int, section: str, key: str) -> str:
    lang = get_language(user_id)
    module = LANG_MODULES.get(lang, LANG_MODULES["ru"]) # дефолтный - русский
    
    # получаем нужную секцию текста (например, buttons, responses)
    section_dict = getattr(module, section, None)
    
    if not section_dict:
        # fallback на русский
        section_dict = getattr(LANG_MODULES["ru"], section, {})
    
    return section_dict.get(key, key)
