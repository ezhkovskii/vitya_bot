
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware, types

from config import settings


class ChatRestrictionMiddleware(BaseMiddleware):
  
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]], event: types.TelegramObject, data: dict[str, Any]
    ) -> Any:
        if event.chat.id == settings.MAIN_CHAT_ID:
            return await handler(event, data)