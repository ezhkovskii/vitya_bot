from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    PACANSKOE_API_URL: str = Field('https://quotes.to.digital/api/random')
    FUCKING_GREAT_ADVICE_API_URL: str = Field('http://fucking-great-advice.ru/api/random')


settings = Settings()