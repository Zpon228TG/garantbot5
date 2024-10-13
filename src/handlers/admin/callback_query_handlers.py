from src.config import dispatcher, bot
from aiogram.types import CallbackQuery, Message
from src.services.database_service import db_service
from src.services.grabber_service import send_message_to_channel
from aiogram.dispatcher.dispatcher import FSMContext
from src.helpers import filters
from aiogram_broadcaster import MessageBroadcaster
import aiogram.utils.exceptions
from src.helpers import states
from src.utils import keyboards


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: msg.data == 'admin', state='*')
async def admin_command_handler(msg: CallbackQuery):
    users_amount = db_service.get_users_amount()
    answer = ('🚀 Админ-панель\n\n'
              f'👥 Пользователей: <b>{users_amount}</b>\n')
    await msg.message.edit_text(text=answer, reply_markup=keyboards.admin)


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: msg.data == 'add_subscription',
                                   filters.UserIsAdmin())
async def add_subscription_to_user_handler(msg: CallbackQuery):
    await states.AddSubscriptionToUser.set_subscription_duration.set()

    answer = '🚀 Выбери длительность подписки'
    await msg.message.edit_text(text=answer, reply_markup=keyboards.subscriptions_duration)


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: 'add_subscription_' in msg.data,
                                   filters.UserIsAdmin(),
                                   state=states.AddSubscriptionToUser.set_subscription_duration)
async def add_subscription_to_user_handler(msg: CallbackQuery, state: FSMContext):
    await states.AddSubscriptionToUser.set_user_id.set()

    subscription_duration = int(msg.data.split('add_subscription_')[1])

    await state.update_data(data={'subscription_duration': subscription_duration})

    answer = (f'🚀 Отправь ID пользователя, '
              f'которому нужно дать подписку на '
              f'{subscription_duration} дней')
    await msg.message.edit_text(text=answer)


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: msg.data == 'takeout_subscription',
                                   filters.UserIsAdmin())
async def takeout_subscription_from_user_handler(msg: CallbackQuery):
    await states.TakeoutSubscriptionFromUser.set_user_id.set()

    answer = '🚀 Отправь ID пользователя, у которого необходимо забрать подписку'
    await msg.message.edit_text(text=answer)


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: msg.data == 'stats', filters.UserIsAdmin(),
                                   state='*')
async def stats_handler(msg: CallbackQuery):
    answer = db_service.get_stats()
    await msg.message.edit_text(text=answer, reply_markup=keyboards.admin)


@dispatcher.callback_query_handler(filters.UserIsAdmin(), lambda msg: msg.data == 'mailing', state='*')
async def mail_handler(msg: CallbackQuery, state: FSMContext):
    answer = '🚀 Отправь сообщение для рассылки (поддерживаются фото, видео, голосовые, кружки, GIF и стикеры)'
    await msg.message.edit_text(text=answer)

    await states.Mailing.set_mailing_message.set()


@dispatcher.callback_query_handler(filters.UserIsAdmin(), state=states.Mailing.set_mailing_message)
async def mail_handler(msg: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message: Message = state_data.get('message')

    if msg.data == 'users' or msg.data == 'all':
        queryset = [_.telegram_id for _ in db_service.get_users()]
        await MessageBroadcaster(queryset, message).run()

    if msg.data == 'channels' or msg.data == 'all':
        queryset = db_service.get_channels()

        for model in queryset:
            await send_message_to_channel(channel_id=model.telegram_channel_id,
                                          text=message.html_text,
                                          video_id=message.video.file_id if message.video else None,
                                          photo_id=message.photo if message.photo else None,
                                          voice_id=message.voice.file_id if message.voice else None,
                                          sticker_id=message.sticker.file_id if message.sticker else None,
                                          animation_id=message.animation.file_id if message.animation else None)

    await msg.message.edit_text(text='⚡️ Рассылка закончена')
