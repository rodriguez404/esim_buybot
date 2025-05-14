from database.models.user import DataBase_User

async def get_user_lang_from_db(user_id: int) -> str:

    user = await DataBase_User.filter(id=user_id).first()
    if user:
        return user.language
    return "ru"