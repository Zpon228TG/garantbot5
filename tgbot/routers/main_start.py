from aiogram import Router, F
from aiogram.types import Message

from ..bot_settings import FSM
from tgbot.keyboards.reply_main import menu_frep
from tgbot.utils.const_functions import ded


router = Router(name=__name__)


# Открытие главного меню
@router.message(F.text.in_(('🔙 Главное меню', '/start')))
async def main_start(message: Message, state: FSM) -> None:
    await state.clear()

    await message.answer(
        text=ded("""
            🔸 Бот готов к использованию.
            🔸 Если не появились вспомогательные кнопки
            🔸 Введите /start
        """),
        reply_markup=menu_frep(message.from_user.id),
    )
