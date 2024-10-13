from src.config import dispatcher
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from src.services.database_service import db_service
from src.services import moderation_service
from src.utils import keyboards
from src.helpers import filters
from src.helpers import exceptions
from src.helpers import states


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(), commands=['start'],
                            state='*')
async def start_command_handler(msg: Message, state: FSMContext):
    await state.finish()

    await msg.answer(text=db_service.get_grabber_menu(msg.from_user.id),
                     reply_markup=keyboards.grabber)


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.Grabber.set_channel)
async def set_channel_handler(msg: Message, state: FSMContext):
    await state.finish()

    answer = '🕒 Добавляю'
    await msg.answer(text=answer)

    try:
        channel_title = await db_service.add_channel(msg.from_user.id, msg.text)

        answer = f'✅ Канал <b>{channel_title}</b> добавлен'
    except exceptions.WaitingIntoTheChannel as exc:
        answer = exc
    await msg.answer(text=answer)


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.Moderation.change_text)
async def change_text_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    post = state_data.get('post')

    await moderation_service.send_to_channel(msg, post)
    await moderation_service.send_post(msg, text=msg.text)

    await state.finish()
