from aiogram import BaseMiddleware
from redis import Redis
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from microservices.get_user_id import get_user_id
from redis_folder.functions.get_user_lang_from_redis import get_user_lang_from_redis
from database.functions.get_user_lang_from_db import get_user_lang_from_db
from redis_folder.redis_client import get_redis
# Единое место обработки языка пользователя для всех хэндлеов
class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        user_id = get_user_id(event)

        if user_id:
            lang = await get_user_lang_from_redis(user_id)
            # Если нет языка пользователя в кэше, ищем в бд
            if not lang:
                lang = await get_user_lang_from_db(user_id)
                if lang and isinstance(get_redis(), Redis):
                    # Найден в бд, но нет в кэше -> запись кэша
                    await get_redis().setex(f"user_lang:{user_id}", 86400, lang)

            data["user_language"] = lang
            return await handler(event, data)

        # Иначе - вернуть дефолт
        data["user_language"] = "ru" # стандартный язык
        return await handler(event, data)