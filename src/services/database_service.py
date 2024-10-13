import datetime
import random
import time
from aiogram.types import Message
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.services.grabber_service import subscribe_to_channel
from src.helpers.sqlalchemy_models import (Base, User, SourceChannel, StopWord,
                                           WordFilter, Postfix, ModeratedMessage)
from src.utils import utils

engine = create_engine('sqlite:///database.db')
# engine = create_engine('postgresql://postgres:1111@0.0.0.0:5432/pixeltype')

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def check_message_moderated(message: SourceChannel):
    if message.is_off:
        return '⚫'
    if message.is_moderated:
        return '🟢'
    return '🔴'


class DatabaseService:
    def __init__(self, session: Session):
        self.session: Session = session

    def create_user(self, telegram_id: str | int):
        if self.session.query(User).filter_by(telegram_id=telegram_id).first() is None:
            self.session.add(User(
                telegram_id=telegram_id
            ))
            self.session.commit()

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(telegram_id=user_id).first()

    def get_moderated_posts(self, user_id: int) -> tuple:
        print(user_id)
        queryset = self.session.query(ModeratedMessage).filter_by(
            user_telegram_id=user_id
        ).all()
        print(queryset)
        if queryset:
            model = random.choice(queryset)
            return model.id, model.telegram_channel_id, model.post_id

    def get_moderated_post(self, post_id: int) -> ModeratedMessage:
        return self.session.query(ModeratedMessage).filter_by(id=post_id).first()

    def get_users(self) -> list[User]:
        return self.session.query(User).distinct().all()

    def get_channels(self) -> list[SourceChannel]:
        return self.session.query(SourceChannel).distinct().all()

    def get_source_channel(self, channel_id: int) -> SourceChannel:
        return self.session.query(SourceChannel).filter_by(telegram_channel_id=channel_id).first()

    def get_users_amount(self) -> int:
        return self.session.query(User).count()

    def get_subscriptions_amount(self) -> int:
        return self.session.query(User).filter(User.subscription_duration is not None).count()

    def add_subscription_to_user(self, user_id: int, subscription_duration: int) -> str:
        """ Add subscription optional duration to user. """

        user = self.session.query(User).filter_by(telegram_id=user_id).first()
        if user:
            user.subscription_duration = subscription_duration * 60 * 60
            user.subscription_start_date = time.time()
            self.session.commit()
            return (f'✅ Пользователю выдана '
                    f'подписка на {subscription_duration} дней')
        return (f'❗️ Пользователю не выдана '
                f'подписка на {subscription_duration} дней: пользователя не существует')

    def takeoff_subscription_from_user(self, user_id: int) -> str:
        user = self.get_user(user_id)
        if user:
            user.subscription_duration = None
            user.subscription_start_date = None
            self.session.commit()
            return (f'✅ У пользователя {user_id} '
                    f'отобрана подписка')
        return '❗️ Пользователя не существует'

    async def check_subscription(self, msg: Message) -> bool:
        user = self.get_user(msg.from_user.id)

        if user.subscription_duration is not None and (
                time.time() - user.subscription_start_date).real >= user.subscription_duration:
            user.subscription_duration = None
            user.subscription_start_date = None
            self.session.commit()

            answer = '🕒 Срок действия вашей подписки истёк'
            await msg.answer(text=answer)

        return user.subscription_duration is not None

    def check_user_channel_exists(self, user_id: int) -> bool:
        return self.get_user(user_id).telegram_channel_id is None

    def get_stats(self) -> str:
        answer = ('🚀 Статистика бота\n\n'
                  f'👥 Кол-во пользователей: {self.get_users_amount()}\n'
                  f'💸 Кол-во подписок: {self.get_subscriptions_amount()}')

        return answer

    async def add_channel(self, user_id: int, channel_link: str) -> tuple:
        channel_id, channel_name = await subscribe_to_channel(channel_link)
        user = self.get_user(user_id)
        user.telegram_channel_link = channel_link
        user.telegram_channel_id = channel_id
        user.telegram_channel_name = channel_name
        self.session.commit()

        return channel_id, channel_name

    async def add_source(self, user_id: int, channel_link: str) -> tuple:
        channel_id, channel_name, last_post = await subscribe_to_channel(channel_link,
                                                                         post=True)

        self.session.add(SourceChannel(
            last_post_id=last_post.id,
            user_telegram_id=user_id,
            telegram_channel_link=channel_link,
            telegram_channel_id=channel_id,
            telegram_channel_name=channel_name
        ))
        self.session.commit()

        return channel_id, channel_name

    def get_last_saved_channel_message(self, channel_id: int):
        source = self.session.query(SourceChannel).filter_by(telegram_channel_id=channel_id).first()
        return source

    def update_last_saved_channel_message(self, channel_id: int, message_id: int):
        model = self.session.query(SourceChannel).filter_by(telegram_channel_id=channel_id).first()
        model.last_post_id = message_id
        self.session.commit()

    def get_user_channel_id(self, user_id: int) -> int:
        user = self.get_user(user_id)
        return user.telegram_channel_id

    def get_grabber_menu(self, user_id: int) -> str:
        user = self.get_user(user_id)
        subscription_expiration = datetime.datetime.fromtimestamp(
            user.subscription_start_date
        ).date() + datetime.timedelta(days=(int(user.subscription_duration / 60 / 60)))

        answer = ('🚀 Персональный граббер\n\n'
                  f'👥 Канал: <b>{user.telegram_channel_name}</b>\n\n'
                  f'🔗 Ссылка: {user.telegram_channel_link}\n\n'
                  f'👑 Подписка на {round(user.subscription_duration / 60 / 60)} дней (до {subscription_expiration}')
        return answer

    def add_stop_word(self, user_id: int, word: str) -> str:
        self.session.add(StopWord(
            word=word,
            user_telegram_id=user_id
        ))
        self.session.commit()

        return self.get_words_filters_menu(user_id)

    def add_word_filter(self, user_id: int,
                        filtered_word: str, substituted_word: str) -> str:
        self.session.add(WordFilter(
            filtered_word=filtered_word,
            substituted_word=substituted_word,
            user_telegram_id=user_id
        ))
        self.session.commit()

        return self.get_words_filters_menu(user_id)

    def add_postfix(self, user_id: int, postfix: str) -> str:
        self.session.add(Postfix(
            postfix=postfix,
            user_telegram_id=user_id
        ))
        self.session.commit()

        return self.get_words_filters_menu(user_id)

    def delete_stop_word(self, stop_word_id: int):
        model = self.session.query(StopWord).filter_by(id=stop_word_id).first()
        self.session.delete(model)
        self.session.commit()

    def delete_source(self, source_id: int):
        model = self.session.query(SourceChannel).filter_by(id=source_id).first()
        self.session.delete(model)
        self.session.commit()

    def delete_moderated_channel(self, moderated_channel_id: int):
        moderated_channel = self.session.query(ModeratedMessage).filter_by(id=moderated_channel_id).first()
        self.session.delete(moderated_channel)
        self.session.commit()

    def delete_word_filter(self, filter_id: int):
        model = self.session.query(WordFilter).filter_by(id=filter_id).first()
        self.session.delete(model)
        self.session.commit()

    def delete_postfix(self, user_id: int):
        model = self.session.query(Postfix).filter_by(user_telegram_id=user_id).all()
        for _ in model:
            self.session.delete(_)
        self.session.commit()

    def get_user_stop_words(self, user_id, _list: bool = False) -> list[StopWord]:
        queryset: list[StopWord] = self.session.query(StopWord).filter_by(user_telegram_id=user_id).all()
        if _list:
            queryset = [stop_word.word for stop_word in queryset]
        return queryset

    def get_user_sources(self, user_id) -> list[SourceChannel]:
        return self.session.query(SourceChannel).filter_by(user_telegram_id=user_id).all()

    def get_user_words_filters(self, user_id) -> list[WordFilter]:
        return self.session.query(WordFilter).filter_by(user_telegram_id=user_id).all()

    def get_postfix(self, user_id: int) -> Postfix | str:
        queryset = self.session.query(Postfix).filter_by(user_telegram_id=user_id).all()
        if len(queryset) > 1:
            return queryset[-1].postfix
        elif queryset:
            return queryset[0].postfix
        return ''

    def get_postfix_menu(self, user_id: int) -> str:
        postfix = self.get_postfix(user_id) if self.get_postfix(user_id) else 'отсутствует'
        answer = f'🚩 <b>Постфикс: </b>{postfix}\n\n'
        return answer

    def get_words_filters_menu(self, user_id: int) -> str:
        stop_words = ', '.join([_.word for _ in self.get_user_stop_words(user_id)]) if self.get_user_stop_words(
            user_id) else 'отсутствуют'

        filters = self.get_user_words_filters(user_id)
        filters_str = '\n\n'

        if filters:
            for _filter in filters:
                filters_str += f'▸ {_filter.filtered_word} → {_filter.substituted_word}\n'
        else:
            filters_str = 'отсутствуют'

        answer = ('⚙️ Фильтрация слов\n\n'
                  f'⛔️ <b>Стоп-слова: </b>{stop_words}\n\n'
                  f'🧹 <b>Фильтры:</b> {filters_str}')
        return answer

    def get_stop_words_reply_markup(self, user_id: int):
        queryset = self.get_user_stop_words(user_id)

        reply_markup = InlineKeyboardMarkup()
        for model in queryset:
            reply_markup.add(InlineKeyboardButton(text=model.word,
                                                  callback_data=model.id))
        reply_markup.add(InlineKeyboardButton(text='⏪ Фильтрация слов',
                                              callback_data='words_filters'))
        return reply_markup

    def get_sources_params_reply_markup(self, user_id: int):
        queryset = self.get_user_sources(user_id)

        reply_markup = InlineKeyboardMarkup()
        for model in queryset:
            reply_markup.add(
                InlineKeyboardButton(text=f'{check_message_moderated(model)} {model.telegram_channel_name}',
                                     callback_data=f'change_moderated_{model.id}'))
        reply_markup.add(InlineKeyboardButton(text='⏪ Источники',
                                              callback_data='sources'))
        return reply_markup

    def get_words_filters_reply_markup(self, user_id: int):
        words_filters = self.get_user_words_filters(user_id)

        reply_markup = InlineKeyboardMarkup()
        for word_filter in words_filters:
            reply_markup.add(InlineKeyboardButton(
                text=f'{word_filter.filtered_word} > {utils.remove_html_tags(word_filter.substituted_word)}',
                callback_data=word_filter.id))
        reply_markup.add(InlineKeyboardButton(text='⏪ Фильтрация слов',
                                              callback_data='words_filters'))
        return reply_markup

    def get_sources_menu(self, user_id: int) -> str:
        sources = '\n'.join([f'▸  <a href="{_.telegram_channel_link}">{_.telegram_channel_name}</a>' for _ in
                             self.get_user_sources(user_id)]) if self.get_user_sources(user_id) \
            else 'отсутствуют'

        answer = ('🔗 Источники\n\n'
                  f'{sources}')
        return answer

    def get_sources_reply_markup(self, user_id: int):
        sources = self.get_user_sources(user_id)

        reply_markup = InlineKeyboardMarkup()
        for source in sources:
            reply_markup.add(InlineKeyboardButton(text=source.telegram_channel_name,
                                                  callback_data=source.id))
        reply_markup.add(InlineKeyboardButton(text='⏪ Фильтрация слов',
                                              callback_data='words_filters'))
        return reply_markup

    def change_moderated_status(self, chanel_id: int):
        channel = self.session.query(SourceChannel).filter_by(id=chanel_id).first()
        if channel.is_moderated and not channel.is_off:
            channel.is_moderated = False
            channel.is_off = True
        elif not channel.is_moderated and channel.is_off:
            channel.is_moderated = False
            channel.is_off = False
        else:
            channel.is_moderated = True
            channel.is_off = False
        self.session.commit()


db_service = DatabaseService(Session())
