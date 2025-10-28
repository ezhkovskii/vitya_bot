from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from config import settings
from bs4 import BeautifulSoup


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


@router.message(Command("fucking_great_advice"))
async def get_fucking_great_advice(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.FUCKING_GREAT_ADVICE_API_URL)
        advice = response.json()
        if advice_text := advice.get('text'):
            await message.reply(advice_text)
        else:
            logger.error(f"Не удалось получить совет: {advice_text}, response_status: {response.status_code}")


@router.message(Command("joke"))
async def get_joke(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.ANEKDOT_API)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        best_rating = -999999
        best_text = ""
        
        for box in soup.find_all('div', class_='topicbox'):
            rates = box.find_next('div', class_='rates')
            text_div = box.find_next('div', class_='text')
            
            if rates and text_div:
                try:
                    rates_text = rates.get('data-r')
                    rates_split_text = rates_text.split(';')
                    positive_count = int(rates_split_text[2])
                    text = text_div.text.strip()
                    if positive_count > best_rating:
                        best_rating = positive_count
                        best_text = text
                except Exception as exc:
                    logger.error(str(exc))

        if best_text:
            await message.reply(best_text)