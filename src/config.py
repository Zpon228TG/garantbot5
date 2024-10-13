from pydantic_settings import BaseSettings
from pyrogram import Client

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone='Europe/Moscow', max_instances=1000)


class Config(BaseSettings):
    TELEGRAM_API_KEY: str
    ADMIN_IDS: list[int] = [6578018656]
    SUBSCRIPTION_ADMIN_USERNAME: str
    USERBOT_USERNAME: str
    BOT_USERNAME: str
    API_ID: int
    API_HASH: str
    USER_SUBSCRIBE_CHANNEL_ID: int = -1002327532594
    USER_SUBSCRIBE_CHANNEL_LINK: str = "https://t.me/grabberX5"

    DAY_1_SUBSCRIPTION_PRICE: int = 250
    DAY_30_SUBSCRIPTION_PRICE: int = 450
    DAY_90_SUBSCRIPTION_PRICE: int = 500
    DAY_365_SUBSCRIPTION_PRICE: int = 1000

    SCHEDULER_TASKS_INTERVAL: int


config = Config(_env_file=".env", _env_file_encoding="utf-8")

bot = Bot(token=config.TELEGRAM_API_KEY, parse_mode='HTML')
dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())

user_app = Client("my_account", api_id=config.API_ID, api_hash=config.API_HASH, )


async def run_client():
    user_app.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_client())

bot_app = Client("my_account", api_id="21619878", api_hash="7229cba001a73991540500b0ba92f463",
                 bot_token="7579905472:AAFAPLUnFR5AeW6gea_8o8QXLD0WqCHhB_o",
                 in_memory=True)
