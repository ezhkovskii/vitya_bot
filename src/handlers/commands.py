from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from config import settings

from log import logger


router = Router()

@router.message(Command("pacanskoe"))
async def get_pacan_quote(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.PACANSKOE_API_URL)
        quote = response.json()
        if quote_text := quote.get('quote'):
            await message.reply(quote_text)
        else:
            logger.error(f"Не удалось получить цитату: {quote}, response_status: {response.status_code}")


# @router.message(Command("all"), F.chat.type.in_({"group", "supergroup"}))
# async def call_all_members(message: Message):
#     rows = await get_users_from_chat(message.chat.id)
#     mentions = [f"@{row['username']}" for row in rows if row["username"]]

#     if not mentions:
#         await message.reply("В чате нет пользователей для упоминания! 🤔")
#         return

#     mention_text = "🔔 Внимание! " + " ".join(mentions)
#     await message.reply(mention_text)