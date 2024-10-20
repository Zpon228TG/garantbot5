from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb


# Открытие своего профиля
def user_profile_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        ikb("💰 Пополнить", data="user_refill"),
        ikb("🎁 Мои покупки", data="user_purchases"),
        ikb("🔗 Реф. система", data="refill")
    )

    return keyboard.adjust(1).as_markup()


def user_payments_kb() -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardBuilder()

    inline_markup.add(
        ikb(text='🔮 ЮMoney', data='user_refill_method:API_Yoomoney'),
        ikb(text='🚀 Tg Cripto', data='user_refill_method:API_Crypto'),
        ikb(text='💎 Crystal', data='user_refill_method:API_Crystal'),
        ikb(text='🧩 AAIO', data='user_refill_method:API_Aaio'),
        ikb(text='🌴 Donation Alerts', data='user_refill_method:API_Donation_alerts')
    )

    return inline_markup.adjust(1).as_markup()


def user_payment_kb(payment_url: str) -> InlineKeyboardMarkup:
    inline_markup = InlineKeyboardBuilder()

    inline_markup.add(
        ikb('Перейти к оплате 💳', payment_url),
        ikb('Проверить оплату ✅', 'check_payment'),
    )

    return inline_markup.adjust(1).as_markup()


# Ссылка на поддержку
def user_support_finl(support_login: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💌 Написать в поддержку", url=f"https://t.me/{support_login}"),
    )

    return keyboard.as_markup()


# Проверка платежа
def refill_bill_finl(pay_link: str, pay_receipt: Union[str, int], pay_way: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🌀 Перейти к оплате", url=pay_link),
    ).row(
        ikb("🔄 Проверить оплату", data=f"Pay:{pay_way}:{pay_receipt}"),
    )

    return keyboard.as_markup()


################################################################################
#################################### ТОВАРЫ ####################################
# Открытие позиции для просмотра
def products_open_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Купить товар", data=f"buy_item_open:{position_id}:{remover}"),
    ).row(
        ikb("🔙 Вернуться", data=f"buy_category_open:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


# Подтверждение покупки товара
def products_confirm_finl(position_id, category_id, get_count) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подтвердить", data=f"buy_item_confirm:{position_id}:{get_count}"),
        ikb("❌ Отменить", data=f"buy_position_open:{position_id}:0"),
    )

    return keyboard.as_markup()


# Возврат к позиции при отмене ввода
def products_return_finl(position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🔙 Вернуться", data=f"buy_position_open:{position_id}:0"),
    )

    return keyboard.as_markup()
