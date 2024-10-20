from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from tgbot.bot_settings import settings
from tgbot.keyboards.reply_main import settings_frep, functions_frep, items_frep
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import get_statistics

router = Router(name=__name__)


# Настройки бота
@router.message(F.text == "⚙️ Настройки")
async def admin_settings(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>⚙️ Основные настройки бота.</b>",
        reply_markup=settings_frep(),
    )


# Общие функции
@router.message(F.text == "🔆 Общие функции")
async def admin_functions(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔆 Выберите нужную функцию.</b>",
        reply_markup=functions_frep(),
    )


# Управление товарами
@router.message(F.text == "🎁 Управление товарами")
async def admin_products(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🎁 Редактирование товаров.</b>",
        reply_markup=items_frep(),
    )


# Cтатистики бота
@router.message(F.text == "📊 Статистика")
async def admin_statistics(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(get_statistics())


# Получение БД
@router.message(Command(commands=['db', 'data_base']))
async def admin_database(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer_document(
        FSInputFile(settings.PATH_DATABASE),
        caption=f"<b>📦 #BACKUP | <code>{get_date(full=False)}</code></b>",
    )
