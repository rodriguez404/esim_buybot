from aiogram.types import Update, Message, CallbackQuery, InlineQuery, PollAnswer, ChatMemberUpdated
# import logging

# Для Middleware универсальная функция получения айдишника пользователя
def get_user_id(event: Update) -> int | None:
    # logging.debug(f"[User ID] Обрабатываем событие {type(event).__name__}")
    # logging.debug(f"[User ID] event.model_dump() = {event.model_dump()}") # очень страшные логи
    
    # Сначала попробуем найти напрямую через from_user
    if hasattr(event, "from_user") and event.from_user and event.from_user.id:
        return event.from_user.id
    # Проверим message (если есть)
    if hasattr(event, "message") and event.message and event.message.from_user and event.message.from_user.id:
        return event.message.from_user.id
    # Проверим callback_query
    if hasattr(event, "callback_query") and event.callback_query and event.callback_query.from_user and event.callback_query.from_user.id:
        return event.callback_query.from_user.id
    # Проверим my_chat_member
    if hasattr(event, "my_chat_member") and event.my_chat_member and event.my_chat_member.from_user and event.my_chat_member.from_user.id:
        return event.my_chat_member.from_user.id
    # Проверим chat (только private чаты)
    if hasattr(event, "chat") and event.chat and event.chat.type == "private" and event.chat.id:
        return event.chat.id

    # Универсальный поиск User в любом месте события
    try:
        for key in event.model_dump().keys():
            value = getattr(event, key, None)
            if value and hasattr(value, "from_user") and value.from_user and value.from_user.id:
                return value.from_user.id
            if value and hasattr(value, "user") and value.user and value.user.id:
                return value.user.id
    except Exception as e:
        pass

    return None