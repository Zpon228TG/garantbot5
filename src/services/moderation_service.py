from src.config import bot
from aiogram.types import CallbackQuery, Message
from src.services.database_service import db_service
from src.config import user_app
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.services import grabber_service


async def send_post(msg: CallbackQuery | Message, text: str = None):
    moderation_post = db_service.get_moderated_posts(msg.from_user.id)
    if moderation_post:
        moderated_message_id, channel_id, message_id = moderation_post
        message = await user_app.get_messages(chat_id=channel_id, message_ids=[message_id, ])

        if message:
            message = message[0]

            if not text:
                text = message.text

            reply_markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text='🗑️ Удалить',
                                     callback_data=f'delete_moderated_post_{moderated_message_id}')
            ).add(
                InlineKeyboardButton(text='⚡️ Заменить текст',
                                     callback_data=f'change_text_moderated_post_{moderated_message_id}')
            ).add(
                InlineKeyboardButton(text='✅ Отправить',
                                     callback_data=f'send_moderated_post_{moderated_message_id}')
            ).add(
                InlineKeyboardButton(text='⏪ Персональный граббер',
                                     callback_data=f'grabber')
            )

            if message.photo:
                await bot.send_photo(chat_id=msg.from_user.id,
                                     caption=text,
                                     photo=message.photo.file_id,
                                     reply_markup=reply_markup)
            elif message.video:
                await bot.send_video(chat_id=msg.from_user.id,
                                     caption=text,
                                     video=message.video.file_id,
                                     reply_markup=reply_markup)
            elif message.voice:
                await bot.send_voice(chat_id=msg.from_user.id,
                                     caption=text,
                                     voice=message.voice.file_id,
                                     reply_markup=reply_markup)
            elif message.sticker:
                await bot.send_sticker(chat_id=msg.from_user.id,
                                       sticker=message.sticker.file_id,
                                       reply_markup=reply_markup)
            elif message.animation:
                await bot.send_animation(chat_id=msg.from_user.id,
                                         caption=text,
                                         animation=message.animation.file_id,
                                         reply_markup=reply_markup)
            else:
                await bot.send_message(chat_id=msg.from_user.id,
                                       text=text,
                                       reply_markup=reply_markup)
        else:
            db_service.delete_moderated_channel(moderated_message_id)
            await send_post(msg)
    else:
        await msg.answer(text='⛔️ Записи на модерации отсутствуют')


async def send_to_channel(msg, post):
    message = await user_app.get_messages(chat_id=post.telegram_channel_id, message_ids=[post.post_id, ])
    if message:
        message = message[-1]

        user_channel_id = db_service.get_user_channel_id(msg.from_user.id)

        text = message.text

        if message.photo:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                photo_id=message.photo.file_id,
                text=text)
        elif message.video:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                video_id=message.video.file_id,
                text=text)
        elif message.animation:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                animation_id=message.animation.file_id,
                text=text)
        elif message.voice:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                voice_id=message.voice.file_id,
                text=text)
        elif message.sticker:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                sticker_id=message.sticker.file_id,
                text=text)
        else:
            await grabber_service.send_message_to_channel(
                channel_id=user_channel_id,
                text=text)
        try:
            await msg.message.delete()
        except AttributeError:
            await msg.delete()

    db_service.delete_moderated_channel(post.post_id)
    await send_post(msg)
