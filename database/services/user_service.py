from tortoise.exceptions import DoesNotExist
from database.models.user import DataBase_User


async def get_user(user_id: int) -> DataBase_User | None:
    try:
        return await DataBase_User.get(id=user_id)
    except DoesNotExist:
        return None

async def create_user(user_id: int, username: str | None = None) -> DataBase_User:
    return await DataBase_User.create(id=user_id, username=username)

async def get_or_create_user(user_id: int, username: str | None = None) -> tuple[DataBase_User, bool]:
    user = await get_user(user_id)
    if user is None:
        user = await create_user(user_id, username)
        return user, True  # True — пользователь создан
    return user, False  # False — уже существовал

