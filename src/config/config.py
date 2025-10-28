from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    ALLOWED_CHATS: list[int]

    PACANSKOE_API_URL: str = 'https://quotes.to.digital/api/random'
    FUCKING_GREAT_ADVICE_API_URL: str = 'http://fucking-great-advice.ru/api/random'
    ANEKDOT_API: str = "https://www.anekdot.ru/random/anekdot/"


settings = Settings()