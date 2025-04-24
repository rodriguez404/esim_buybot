from loader import cache, router
from aiogram import types

@router.message()
async def show_cached_data(message: types.Message):
    user_id = str(message.from_user.id)

    # Попробуем достать кэш
    cached = await cache.get(f"user:{user_id}")
    if cached:
        await message.answer(f"Из кэша: {cached}")
    else:
        # Эмуляция получения данных
        data = {"greeting": "Привет!", "id": user_id}
        await cache.set(f"user:{user_id}", data, ttl=120)
        await message.answer(f"Данные загружены и закэшированы: {data}")