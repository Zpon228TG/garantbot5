from datetime import datetime

from aiogram import Bot
from aiogram.types import FSInputFile

from tgbot.bot_settings import settings, ARS
from tgbot.data_base.db_category import Categoryx
from tgbot.data_base.db_item import Itemx
from tgbot.data_base.db_position import Positionx, PositionModel
from tgbot.data_base.db_settings import Settingsx
from tgbot.data_base.db_users import Userx
from tgbot.utils.const_functions import get_unix, get_date, ded, send_admins
from tgbot.utils.text_functions import get_statistics


# Уведомление и проверка обновления при запуске бота
async def startup_notify(bot: Bot) -> None:
    if len([settings.ADMIN_ID]) >= 1:
        await send_admins(
            bot,
            ded(f"""
                <b>✅ Бот был успешно запущен</b>
                ➖➖➖➖➖➖➖➖➖➖
                <code>❗ Данное сообщение видят только администраторы бота.</code>
            """),
        )


# Автоматическая очистка ежедневной статистики после 00:00:15
async def update_profit_day(bot: Bot):
    await send_admins(bot, get_statistics())

    Settingsx.update(misc_profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:00:10
async def update_profit_week():
    Settingsx.update(misc_profit_week=get_unix())


# Автоматическое обновление счётчика каждый месяц первого числа в 00:00:05
async def update_profit_month():
    Settingsx.update(misc_profit_month=get_unix())


# Проверка на перенесение БД из старого бота в нового или указание токена нового бота
async def check_bot_username(bot: Bot):
    get_login = Settingsx.get()
    get_bot = await bot.get_me()

    if get_bot.username != get_login.misc_bot:
        Settingsx.update(misc_bot=get_bot.username)


# Автобэкапы БД для админов
async def autobackup_admin(bot: Bot):
    for admin in [settings.ADMIN_ID]:
        try:
            await bot.send_document(
                admin,
                FSInputFile(settings.PATH_DATABASE),
                caption=f"<b>📦 #BACKUP | <code>{get_date(full=False)}</code></b>",
                disable_notification=True,
            )
        except:
            ...


# Вставка тэгов юзера в текст
def insert_tags(user_id: int | str, text: str) -> str:
    get_user = Userx.get(user_id=user_id)

    if "{user_id}" in text:
        text = text.replace("{user_id}", f"<b>{get_user.user_id}</b>")
    if "{username}" in text:
        text = text.replace("{username}", f"<b>{get_user.user_login}</b>")
    if "{firstname}" in text:
        text = text.replace("{firstname}", f"<b>{get_user.user_name}</b>")

    return text


# Наличие товаров
def get_items_available() -> list[str]:
    get_categories = Categoryx.get_all()
    save_items = []

    for category in get_categories:
        get_positions = Positionx.gets(category_id=category.category_id)

        if len(get_positions) >= 1:
            cache_items = [f'<b>➖➖➖ {category.category_name} ➖➖➖</b>']

            for position in get_positions:
                if len(cache_items) < 30:
                    get_items = Itemx.gets(position_id=position.position_id)

                    if len(get_items) >= 1:
                        cache_items.append(
                            f"{position.position_name} | {position.position_price}₽ | В наличии {len(get_items)} шт",
                        )
                else:
                    save_items.append("\n".join(cache_items))
                    cache_items = [f'<b>➖➖➖ {category.category_name} ➖➖➖</b>']

            if len(cache_items) > 1:
                save_items.append("\n".join(cache_items))

    return save_items


# Получение позиций с товарами
def get_positions_items(category_id: str | int) -> list[PositionModel]:
    get_settings = Settingsx.get()

    get_positions = Positionx.gets(category_id=category_id)

    save_positions = []

    if get_settings.misc_item_hide == "True":
        for position in get_positions:
            get_items = Itemx.gets(position_id=position.position_id)

            if len(get_items) >= 1:
                save_positions.append(position)
    else:
        save_positions = get_positions

    return save_positions


# Авто-настройка UNIX времени в БД
async def autosettings_unix():
    now_day = datetime.now().day
    now_week = datetime.now().weekday()
    now_month = datetime.now().month
    now_year = datetime.now().year

    unix_day = int(datetime.strptime(f"{now_day}.{now_month}.{now_year} 0:0:0", "%d.%m.%Y %H:%M:%S").timestamp())
    unix_week = unix_day - (now_week * 86400)
    unix_month = int(datetime.strptime(f"1.{now_month}.{now_year} 0:0:0", "%d.%m.%Y %H:%M:%S").timestamp())

    Settingsx.update(
        misc_profit_day=unix_day,
        misc_profit_week=unix_week,
        misc_profit_month=unix_month,
    )
