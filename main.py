import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from tgbot.bot_settings import BOT_SCHEDULER, Logger, DarkShop_bot
from tgbot.data_base.db_helper import create_dbx
from tgbot.middlewares import register_all_middlwares
from tgbot.routers import register_all_routers
from tgbot.services.api_session import AsyncRequestSession
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.utils.misc_functions import *
from tgbot.services.api_aaio import AaioAPI
from tgbot.bot_settings import settings, payment_systems

# Инициализация API AAIO
api_aio = AaioAPI(
    aaio_secret_key=settings.AAIO_SECRET_KEY.get_secret_value(),
    aaio_id_shop=settings.AAIO_ID_SHOP,
    aaio_api_key=settings.AAIO_API_KEY.get_secret_value()
)

# Добавление API Aaio в словарь payment_systems
payment_systems['API_Aaio'] = api_aio

# Запуск планировщика.
async def scheduler_start(bot: Bot) -> None:
    BOT_SCHEDULER.add_job(update_profit_month, trigger="cron", day=1, hour=0, minute=0, second=5)
    BOT_SCHEDULER.add_job(update_profit_week, trigger="cron", day_of_week="mon", hour=0, minute=0, second=10)
    BOT_SCHEDULER.add_job(update_profit_day, trigger="cron", hour=0, minute=0, second=15, args=(bot,))
    BOT_SCHEDULER.add_job(autobackup_admin, trigger="cron", hour=0, args=(bot,))

# Запуск бота и базовых функций
async def main():
    BOT_SCHEDULER.start()
    dp = Dispatcher()
    ar_session = AsyncRequestSession()
    
    register_all_middlwares(dp)
    register_all_routers(dp)

    Logger.info('Bot successfully started!')

    try:
        await autosettings_unix()
        await set_commands(DarkShop_bot)
        await check_bot_username(DarkShop_bot)
        await startup_notify(DarkShop_bot, ar_session)
        await scheduler_start(DarkShop_bot)

        await DarkShop_bot.delete_webhook()
        await DarkShop_bot.get_updates(offset=-1)

        await dp.start_polling(
            DarkShop_bot,
            allowed_updates=dp.resolve_used_update_types(),
            arSession=ar_session,
        )
    finally:
        await ar_session.close()
        await DarkShop_bot.session.close()

if __name__ == "__main__":
    create_dbx()

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        Logger.info('Bot successfully stopped!')
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
