from src.config import bot
from src.services.grabber_service import get_last_channel_message
from src.services.database_service import db_service
from src.helpers.sqlalchemy_models import SourceChannel, WordFilter, ModeratedMessage
from src.services import grabber_service


def set_filters_to_text(user_id: int, text: str) -> str:
    filters: list[WordFilter] = db_service.get_user_words_filters(user_id)
    for _filter in filters:
        text = text.replace(_filter.filtered_word, _filter.substituted_word)
    return text


def check_stop_words(user_id: int, text):
    for stop_word in db_service.get_user_stop_words(user_id, _list=True):
        if stop_word in text or stop_word in text:
            return True


async def check_channels_task():
    tasks = db_service.session.query(SourceChannel).all()

    for task in tasks:
        user_id = task.user_telegram_id
        channel_id = task.telegram_channel_id
        channel = db_service.get_source_channel(channel_id)

        if not channel.is_off:
            last_channel_message = await get_last_channel_message(channel_id=channel_id)
            last_saved_channel_message = db_service.get_last_saved_channel_message(channel_id=channel_id)

            if last_channel_message.text:
                if check_stop_words(user_id,
                                    last_channel_message.text
                                    if last_channel_message.text else last_channel_message.caption):
                    return None

                text = set_filters_to_text(user_id,
                                           last_channel_message.text
                                           if last_channel_message.text else last_channel_message.caption)

                text += f'\n\n{db_service.get_postfix(user_id)}'
            else:
                text = None

            if channel.is_moderated:
                if not db_service.session.query(ModeratedMessage).filter_by(telegram_channel_id=channel_id,
                                                                            post_id=last_channel_message.id).first():
                    db_service.session.add(ModeratedMessage(
                        user_telegram_id=user_id,
                        telegram_channel_id=channel_id,
                        post_id=last_channel_message.id,
                        post_text=text
                    ))
                    db_service.session.commit()
            else:

                if last_channel_message.id != last_saved_channel_message.last_post_id:
                    db_service.update_last_saved_channel_message(channel_id=channel_id,
                                                                 message_id=last_channel_message.id)
                    if last_saved_channel_message.is_moderated:
                        ...
                    else:
                        user_channel_id = db_service.get_user_channel_id(user_id)

                        if last_channel_message.photo:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                photo_id=last_channel_message.photo.file_id,
                                text=text)
                        elif last_channel_message.video:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                video_id=last_channel_message.video.file_id,
                                text=text)
                        elif last_channel_message.animation:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                animation_id=last_channel_message.animation.file_id,
                                text=text)
                        elif last_channel_message.voice:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                voice_id=last_channel_message.voice.file_id,
                                text=text)
                        elif last_channel_message.sticker:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                sticker_id=last_channel_message.sticker.file_id,
                                text=text)
                        else:
                            await grabber_service.send_message_to_channel(
                                channel_id=user_channel_id,
                                text=text)
