import asyncio
import os
import shutil
import tempfile

from aiogram import Bot, Router, F
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message, FSInputFile
from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge

from log import logger


router = Router()



@router.message(
    F.chat.type == "private",
    (F.video | F.audio | F.document),
)
async def convert_media_to_voice(message: Message, bot: Bot):
    """
    Принимает аудио/видео от пользователя в личном чате и отправляет обратно голосовое сообщение.
    """

    media = None

    if message.video:
        media = message.video
    elif message.audio:
        media = message.audio
    elif message.document and message.document.mime_type:
        if message.document.mime_type.startswith("audio/") or message.document.mime_type.startswith("video/"):
            media = message.document

    if not media:
        return

    temp_dir = tempfile.mkdtemp(prefix="vitya_media_")
    input_path = os.path.join(temp_dir, "input")
    output_path = os.path.join(temp_dir, "voice.ogg")

    try:
        file_info = await bot.get_file(media.file_id)
        await bot.download_file(file_info.file_path, destination=input_path)

        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vn",
            "-acodec",
            "libopus",
            "-b:a",
            "24k",
            "-ar",
            "16000",
            "-ac",
            "1",
            output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()

        if process.returncode != 0 or not os.path.exists(output_path):
            logger.error(f"ffmpeg convert error: {stderr.decode(errors='ignore')}")
            await message.reply("Не получилось обработать файл :(")
            return

        voice = FSInputFile(output_path, filename="voice_message.ogg")
        await message.answer_voice(voice)
    except Exception as exc:
        await message.reply(f"Произошла ошибка при обработке файла: {exc}")
        logger.error(f"Error while converting media to voice: {exc}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
