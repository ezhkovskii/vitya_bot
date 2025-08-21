from aiogram import Bot, Router, F
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message

from log import logger


router = Router()


# @router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
# async def track_chat_members_join(event: ChatMemberUpdated, bot: Bot):
#     chat = event.chat
#     new_chat_member = event.new_chat_member.user

#     # Если бот был добавлен в чат — сохраняем чат
#     if new_chat_member.id == bot.id:
#         logger.info(f'Join bot to chat {chat.id}')
#         await add_chat(chat.id, chat.title)
#         return

#     # Пользователь присоединился
#     logger.info(f'Join user {new_chat_member.id} to chat {chat.id}')
#     await add_user(new_chat_member.id, chat.id, new_chat_member.username, new_chat_member.first_name, new_chat_member.last_name)


# @router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
# async def track_chat_members_leave(event: ChatMemberUpdated, bot: Bot):
#     chat = event.chat
#     left_user = event.new_chat_member.user

#     if left_user.id == bot.id:
#         logger.info(f'Delete bot from chat {chat.id}')
#         await delete_chat(chat.id)
#         return

#     # Пользователь покинул чат — удаляем связь user ↔ chat
#     logger.info(f'Remove user {left_user.id} from chat {chat.id}')
#     await remove_user(left_user.id, chat.id)


# @router.message(F.chat.type.in_({"group", "supergroup"}) & ~F.new_chat_member & ~F.left_chat_member & ~F.text.startswith('/'))
# async def track_first_message(message: Message):
#     chat = message.chat
#     user = message.from_user
#     if not await exists_user_in_chat(user.id, chat.id):
#         logger.info(f'Add user {user.id} to chat {chat.id}')
#         await add_user(user.id, chat.id, user.username, user.first_name, user.last_name)
