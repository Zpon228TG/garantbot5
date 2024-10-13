import time

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from src.helpers.mixins import SqlalchemySerializerMixin, SqlalchemyTableMixin

Base = declarative_base()


class User(Base, SqlalchemySerializerMixin, SqlalchemyTableMixin):
    """ Bot user. """

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)

    telegram_channel_name = Column(String)
    telegram_channel_link = Column(String)
    telegram_channel_id = Column(Integer)

    subscription_duration = Column(Integer)
    subscription_start_date = Column(Integer)


class SourceChannel(Base, SqlalchemySerializerMixin, SqlalchemyTableMixin):
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)

    is_off = Column(Boolean, default=False)

    is_moderated = Column(Boolean, default=False)

    telegram_channel_name = Column(String)
    telegram_channel_link = Column(String)
    telegram_channel_id = Column(Integer)

    last_post_id = Column(Integer)


class MandatorySubscriptionChannels(Base,
                                    SqlalchemySerializerMixin,
                                    SqlalchemyTableMixin):
    """ Mandatory subscription channels. """

    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(Integer)
    link = Column(String)


class StopWord(Base,
               SqlalchemySerializerMixin,
               SqlalchemyTableMixin):
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)

    word = Column(String)


class WordFilter(Base,
                 SqlalchemySerializerMixin,
                 SqlalchemyTableMixin):
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)

    filtered_word = Column(String)
    substituted_word = Column(String)


class Postfix(Base,
              SqlalchemySerializerMixin,
              SqlalchemyTableMixin):
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)

    postfix = Column(String)


class ModeratedMessage(Base,
                       SqlalchemySerializerMixin,
                       SqlalchemyTableMixin):
    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)
    telegram_channel_id = Column(Integer)
    post_id = Column(Integer)

    post_text = Column(String)
