from database.services.user_service import get_user_from_db


async def update_user_language_in_db(user_id: int, new_language: str) -> bool:
    user = await get_user_from_db(user_id)
    if not user:
        return False  # Пользователь не найден

    user.language = new_language
    await user.save()
    return True