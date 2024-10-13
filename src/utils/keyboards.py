from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.config import config

everyone_delete = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🗑️ Удалить упоминание',
                         callback_data='trainings'))

subscribe_channel = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='Подписаться на канал',
                         url=config.USER_SUBSCRIBE_CHANNEL_LINK)
).add(
    InlineKeyboardButton(text='🚀 Я подписался',
                         url='https://t.me/' + config.BOT_USERNAME + '?start=start')
)

buy_subscription = InlineKeyboardMarkup().add(InlineKeyboardButton(
    text='🛒 Купить подписку',
    url='https://t.me/' + config.SUBSCRIPTION_ADMIN_USERNAME
))

admin = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🚀 Дать подписку',
                         callback_data='add_subscription')
).add(
    InlineKeyboardButton(text='🗑️ Забрать подписку',
                         callback_data='takeout_subscription')
).add(
    InlineKeyboardButton(text='💬 Рассылка',
                         callback_data='mailing')
).add(
    InlineKeyboardButton(text='📊 Статистика',
                         callback_data='stats')
).add(
    InlineKeyboardButton(text='⏪ Персональный граббер',
                         callback_data='grabber')
)

subscriptions_duration = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🕒 1 день',
                         callback_data='add_subscription_1')
).add(
    InlineKeyboardButton(text='🕒 30 дней',
                         callback_data='add_subscription_30')
).add(
    InlineKeyboardButton(text='🕒 90 дней',
                         callback_data='add_subscription_90')
).add(
    InlineKeyboardButton(text='🕒 1 год',
                         callback_data='add_subscription_365')
).add(
    InlineKeyboardButton(text='⏪ Админ панель',
                         callback_data='admin')
)

grabber = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='📊️ Посты на модерации',
                         callback_data='moderation_posts')
).add(
    InlineKeyboardButton(text='⚙️ Настройки граббера',
                         callback_data='grabber_settings')
).add(
    InlineKeyboardButton(text='🗑️ Сменить канал',
                         callback_data='change_channel')
)

grabber_settings = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🔗 Источники',
                         callback_data='sources')
).add(
    InlineKeyboardButton(text='⚙️ Фильтрация слов',
                         callback_data='words_filters'),
    InlineKeyboardButton(text='⚙️ Постфикс',
                         callback_data='postfix')
).add(
    InlineKeyboardButton(text='⏪ Персональный граббер',
                         callback_data='grabber')
)

words_filters = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='➕ Добавить стоп-слова',
                         callback_data='add_stop_word')
).add(
    InlineKeyboardButton(text='🗑️ Удалить стоп-слова',
                         callback_data='delete_stop_word')
).add(
    InlineKeyboardButton(text='➕ Добавить фильтр',
                         callback_data='add_word_filter')
).add(
    InlineKeyboardButton(text='🗑️ Удалить фильтр',
                         callback_data='delete_word_filter')
).add(
    InlineKeyboardButton(text='⏪ Настройки граббера',
                         callback_data='grabber_settings')
)

postfix = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='➕ Установить постфикс',
                         callback_data='set_postfix')
).add(
    InlineKeyboardButton(text='🗑️ Удалить постфикс',
                         callback_data='delete_postfix')
).add(
    InlineKeyboardButton(text='⏪ Настройки граббера',
                         callback_data='grabber_settings')
)

sources = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='➕ Добавить источник',
                         callback_data='add_source')
).add(
    InlineKeyboardButton(text='🗑️ Удалить источник',
                         callback_data='delete_source')
).add(
    InlineKeyboardButton(text='⚙️ Параметры источников',
                         callback_data='source_params')
).add(
    InlineKeyboardButton(text='⏪ Настройки граббера',
                         callback_data='grabber_settings')
)

mailing = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text='🚀 Только пользователи',
                         callback_data='users')
).add(
    InlineKeyboardButton(text='🚀 Только по каналам',
                         callback_data='channels')
).add(
    InlineKeyboardButton(text='🚀 Везде',
                         callback_data='all')
).add(
    InlineKeyboardButton(text='⏪ Админ панель',
                         callback_data='admin')
)
