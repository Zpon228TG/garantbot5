import sqlite3

from pydantic import BaseModel

from tgbot.bot_settings import settings
from tgbot.data_base.db_helper import dict_factory, update_format


# Модель таблицы
class SettingsModel(BaseModel):
    status_work: str
    status_refill: str
    status_buy: str
    misc_faq: str
    misc_support: str
    misc_bot: str
    misc_item_hide: str
    misc_profit_day: int
    misc_profit_week: int
    misc_profit_month: int


# Работа с настройками
class Settingsx:
    storage_name = "storage_settings"

    # Получение записи
    @staticmethod
    def get() -> SettingsModel:
        with sqlite3.connect(settings.PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Settingsx.storage_name}"

            return SettingsModel(**con.execute(sql).fetchone())

    # Редактирование записи
    @staticmethod
    def update(**kwargs):
        with sqlite3.connect(settings.PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Settingsx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)

            con.execute(sql, parameters)
