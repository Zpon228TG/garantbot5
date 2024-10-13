from src.config import user_app
from pydantic import BaseModel
from pyrogram.types import ChatPreview
from src.helpers import exceptions
import pyrogram.errors.exceptions


class ChatMember(BaseModel):
    user_id: int
    first_name: str
    username: str | None = None


async def get_last_channel_message(channel_id):
    post = None

    history = user_app.get_chat_history(chat_id=channel_id, limit=1)

    async for _ in history:
        post = _

    return post


async def subscribe_to_channel(channel_link: str, post: bool = False):
    try:
        channel_info = await user_app.get_chat(channel_link)
    except:
        try:
            await user_app.join_chat(channel_link)
        except pyrogram.errors.exceptions.bad_request_400.UserAlreadyParticipant:
            ...

        channel_info = await user_app.get_chat(channel_link)
    try:
        await user_app.join_chat(channel_link)
    except:
        pass

    if type(channel_info) == ChatPreview:
        detail = ('Заявка на вступление в приватный канал ботом подана. '
                  'Отправьте ту же ссылку чуть позже, когда заявка '
                  'будет рассмотрена')
        raise exceptions.WaitingIntoTheChannel(detail)

    channel_name = channel_info.title
    channel_id = channel_info.id
    if post:
        last_post = await get_last_channel_message(channel_id=channel_id)
        return channel_id, channel_name, last_post
    return channel_id, channel_name


async def send_message_to_channel(channel_id: int, text: str,
                                  photo_id = None,
                                  video_id: str = None,
                                  voice_id: str = None,
                                  animation_id: str = None,
                                  sticker_id: str = None):
    if photo_id:
        await user_app.send_photo(chat_id=channel_id,
                                  photo=photo_id,
                                  caption=text)
    elif video_id:
        await user_app.send_video(chat_id=channel_id,
                                  video=video_id,
                                  caption=text)
    elif animation_id:
        await user_app.send_animation(chat_id=channel_id,
                                      animation=voice_id,
                                      caption=text)
    elif sticker_id:
        await user_app.send_sticker(chat_id=channel_id,
                                    sticker=sticker_id)
    else:
        await user_app.send_message(chat_id=channel_id,
                                    text=text)
