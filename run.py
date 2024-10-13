from src.config import dispatcher, bot
from aiogram.utils import executor
from aiogram.types import BotCommand
from src.handlers.admin import message_handlers
from src.handlers.admin import callback_query_handlers
from src.handlers.grabber import message_handlers
from src.handlers.grabber import callback_query_handlers
from src.handlers.grabber_settings import message_handlers
from src.handlers.grabber_settings import callback_query_handlers

import logging

logging.basicConfig(filename='logs.log', filemode='w')


async def set_commands(dp):
    await bot.set_my_commands(commands=[
        BotCommand('start', description='Главное меню'),
    ])


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=set_commands)
