from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import SecretStr

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext

from tgbot.services.api_session import AsyncRequestSession
from .services import api_donation_alerts, api_aaio, api_crypto_bot, api_crystal, api_yoomoney


class Settings(BaseSettings):
    TELEGRAM_API_TOKEN: SecretStr
    BOT_TIMEZONE: str
    PATH_DATABASE: str
    REVIEW_URL: SecretStr
    ADMIN_ID: int
    LOGS_UR: SecretStr

    AAIO_SECRET_KEY: SecretStr
    AAIO_ID_SHOP: int
    AAIO_API_KEY: SecretStr

    CRYPTO_BOT_API_TOKEN: SecretStr

    CRYSTAL_LOGIN: str
    CRYSTAL_API_TOKEN: SecretStr

    DONATION_ALERTS_API_TOKEN: SecretStr

    YOOMONEY_API_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")


settings = Settings()


DarkShop_bot = Bot(token=settings.TELEGRAM_API_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))


payment_systems: dict[str, any] = {
    'API_Crypto': api_crypto_bot.API_Crypto,
    'API_Crystal': api_crystal.API_Crystal,
    'API_Aaio': api_aaio.API_AAIO,
    'API_Donation_alerts': api_donation_alerts.API_Donation_alerts,
    'API_Yoomoney': api_yoomoney.API_Yoomoney
}


BOT_SCHEDULER = AsyncIOScheduler(timezone=settings.BOT_TIMEZONE)
FSM = FSMContext
ARS = AsyncRequestSession
Logger = logger
