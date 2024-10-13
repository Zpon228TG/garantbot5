from aiogram.dispatcher.dispatcher import FSMContext
from src.config import dispatcher, bot
from aiogram.types import Message
from src.services.database_service import db_service
from src.helpers import filters
from src.utils import keyboards
from src.helpers import states


@dispatcher.message_handler(filters.UserIsAdmin(), commands=['admin'], state='*')
async def admin_command_handler(msg: Message):
    users_amount = db_service.get_users_amount()
    answer = ('🚀 Админ-панель\n\n'
              f'👥 Пользователей: <b>{users_amount}</b>\n')
    await msg.answer(text=answer, reply_markup=keyboards.admin)


@dispatcher.message_handler(filters.UserIsAdmin(), state=states.AddSubscriptionToUser.set_user_id)
async def add_subscription_to_user_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    subscription_duration = state_data.get('subscription_duration')

    answer = db_service.add_subscription_to_user(msg.text, subscription_duration)
    user_answer = f'🚀 Вам выдана подписка на {subscription_duration} дней'
    await bot.send_message(text=user_answer,
                           chat_id=msg.text)
    await msg.answer(text=answer)

    await state.finish()


@dispatcher.message_handler(filters.UserIsAdmin(), state=states.TakeoutSubscriptionFromUser.set_user_id)
async def takeout_subscription_from_user_handler(msg: Message, state: FSMContext):
    answer = db_service.takeoff_subscription_from_user(msg.text)
    await msg.answer(text=answer, reply_markup=keyboards.admin)
    await state.finish()


@dispatcher.message_handler(filters.UserIsAdmin(),
                            content_types=['photo', 'voice', 'video', 'video_message', 'animation', 'sticker',
                                           'text'], state=states.Mailing.set_mailing_message)
async def mail_handler(msg: Message, state: FSMContext):
    await state.update_data(data={'message': msg})

    answer = '🚀 Выбери тип рассылки'
    await msg.answer(text=answer, reply_markup=keyboards.mailing)
