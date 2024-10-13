from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
from src.services.database_service import db_service
from src.helpers import states
from src.config import config
from src.utils import keyboards
from src.config import bot
import aiogram


class UserIsAdmin(BoundFilter):
    async def check(self, msg: CallbackQuery | Message):
        return msg.from_user.id in config.ADMIN_IDS


class UserWithSubscribe(BoundFilter):
    async def check(self, msg: CallbackQuery | Message):
        if await UserIsAdmin().check(msg):
            return True

        db_service.create_user(msg.from_user.id)

        if not await db_service.check_subscription(msg):
            answer = ('🚀 Для получения доступа к функционалу необходимо приобрести подписку. '
                      'Напишите администратору, нажав на кнопку.')
            if type(msg) is CallbackQuery:
                await msg.message.edit_text(text=answer, reply_markup=keyboards.buy_subscription)
            else:
                await msg.answer(text=answer, reply_markup=keyboards.buy_subscription)
            return False
        if db_service.check_user_channel_exists(msg.from_user.id):
            answer = ("🚀 Отправь ссылку на твой канал (вида <a href='t.me'> https://t.me/...</a> или @ChanelName) "
                      "и сделай администратором в нём "
                      f"аккаунт @{config.USERBOT_USERNAME}")
            await msg.answer(text=answer)
            await states.Grabber.set_channel.set()

            return False

        return True


class UserIsChannelSubscriber(BoundFilter):
    async def check(self, msg: Message):
        if config.USER_SUBSCRIBE_CHANNEL_ID:
            try:
                is_subscribed = await bot.get_chat_member(config.USER_SUBSCRIBE_CHANNEL_ID, msg.from_user.id)

                if is_subscribed.is_chat_member():
                    if (is_subscribed.status == 'member' or
                            is_subscribed.status == 'administrator' or
                            is_subscribed.status == 'creator'):
                        return True
                await msg.answer('❗️ Вы не подписаны на канал',
                                 reply_markup=keyboards.subscribe_channel)
                return False
            except aiogram.utils.exceptions.ChatNotFound:
                user_answer = '❗️ Возникла проблема. Чиним.'
                admin_answer = '❗️ Бот не добавлен в указанный для подписки канал'

                await msg.answer(text=user_answer)
                await bot.send_message(chat_id=config.ADMIN_ID,
                                       text=admin_answer)
        else:
            return True
