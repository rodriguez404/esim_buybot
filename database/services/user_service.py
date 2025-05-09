from tortoise.exceptions import DoesNotExist
from database.models.user import DataBase_User
from aiogram.types import User as TelegramUser

SUPPORTED_LANGUAGES = {"en", "ru"}

async def get_user(user_id: int) -> DataBase_User | None:
    try:
        return await DataBase_User.get(id=user_id)
    except DoesNotExist:
        return None

async def create_user(user_id: int, username: str | None = None, language: str = "en") -> DataBase_User:
    return await DataBase_User.create(id=user_id, username=username, language=language)

async def get_or_create_user(telegram_user: TelegramUser) -> tuple[DataBase_User, bool]:
    user = await get_user(telegram_user.id)
    if user is None:
        # Язык по умолчанию — из Telegram, если он поддерживается
        lang = telegram_user.language_code if telegram_user.language_code in SUPPORTED_LANGUAGES else "en"
        user = await create_user(telegram_user.id, telegram_user.username, lang)
        return user, True  # True — пользователь создан
    return user, False  # False — уже существовал

