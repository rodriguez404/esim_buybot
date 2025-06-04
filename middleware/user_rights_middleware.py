from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from config import ADMINS

from microservices.get_user_id import get_user_id

import time, logging

# Мидлварь для проверки уровня доступа пользователя (дефолт или админ)
class UserRightsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        starting_global_time = time.time()

        data["user_rights"] = "default"

        user_id = get_user_id(event)
        if user_id in ADMINS:
            data["user_rights"] = "admin"

        duration = (time.time() - starting_global_time) * 1000  # в мс
        logging.debug(f"[DEBUG]: [UserRightMiddleware] work time: {duration:.2f} ms")
        return await handler(event, data)