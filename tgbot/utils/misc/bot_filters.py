from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from tgbot.bot_settings import settings
from tgbot.data_base.db_settings import Settingsx


# Проверка на админа
class IsAdmin(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:
        if update.from_user.id in [settings.ADMIN_ID]:
            return True
        else:
            return False


# Проверка на технические работы
class IsWork(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:
        get_settings = Settingsx.get()

        if get_settings.status_work == "False" or update.from_user.id in [settings.ADMIN_ID]:
            return False
        else:
            return True


# Проверка на возможность пополнения
class IsRefill(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:
        get_settings = Settingsx.get()

        if get_settings.status_refill == "True" or update.from_user.id in [settings.ADMIN_ID]:
            return False
        else:
            return True


# Проверка на возможность покупки товара
class IsBuy(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery, bot: Bot) -> bool:
        get_settings = Settingsx.get()

        if get_settings.status_buy == "True" or update.from_user.id in [settings.ADMIN_ID]:
            return False
        else:
            return True
