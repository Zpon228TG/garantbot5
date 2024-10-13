from src.config import dispatcher
from aiogram.types import CallbackQuery
from src.helpers import states
from src.services.database_service import db_service
from aiogram.dispatcher.dispatcher import FSMContext
from src.services import moderation_service
from src.utils import keyboards
from src.helpers import filters
from src.config import config, user_app


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'change_channel')
async def change_channel_handler(msg: CallbackQuery):
    answer = ("🚀 Отправь ссылку на твой канал (вида <a href='t.me'> https://t.me/...</a> или @ChanelName) "
              "и сделай администратором в нём "
              f"аккаунт @{config.USERBOT_USERNAME}")
    await msg.message.edit_text(text=answer)
    await states.Grabber.set_channel.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'moderation_posts')
async def moderated_handler(msg: CallbackQuery):
    answer = '🟢 Посты на модерации'
    await msg.message.edit_text(text=answer, reply_markup=keyboards.words_filters)

    await moderation_service.send_post(msg)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data.startswith('delete_moderated_post_'))
async def moderated_handler(msg: CallbackQuery):
    db_service.delete_moderated_channel(msg.data.split('delete_moderated_post_')[1])
    await msg.message.delete()
    await moderation_service.send_post(msg)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data.startswith('send_moderated_post_'))
async def moderated_handler(msg: CallbackQuery):
    post_id = int(msg.data.split('send_moderated_post_')[1])
    post = db_service.get_moderated_post(post_id)

    await moderation_service.send_to_channel(msg, post)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data.startswith('change_text_moderated_post_'))
async def moderated_handler(msg: CallbackQuery, state: FSMContext):
    post_id = int(msg.data.split('change_text_moderated_post_')[1])
    post = db_service.get_moderated_post(post_id)

    await msg.message.answer(text='🚀 Отправь новый текст')
    await states.Moderation.change_text.set()

    await state.update_data(data={'post': post})
