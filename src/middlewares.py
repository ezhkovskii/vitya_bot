
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware, types

from config import settings
from log import logger


class ChatRestrictionMiddleware(BaseMiddleware):
  
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]], event: types.TelegramObject, data: dict[str, Any]
    ) -> Any:
        logger.info(f"Chat ID: {event.chat.id}, Chat title: {event.chat.title or event.chat.username}")
        if event.chat.id in settings.ALLOWED_CHATS:
            return await handler(event, data)