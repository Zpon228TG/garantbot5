from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin(StatesGroup):
    ...


class AddSubscriptionToUser(StatesGroup):
    set_user_id = State()
    set_subscription_duration = State()


class TakeoutSubscriptionFromUser(StatesGroup):
    set_user_id = State()


class Grabber(StatesGroup):
    set_channel = State()

    set_prefix = State()
    set_postfix = State()


class GrabberSettings(StatesGroup):
    add_source = State()
    delete_source = State()

    add_stop_word = State()
    delete_stop_word = State()

    add_filter_filtered_word = State()
    add_filter_substituted_word = State()
    delete_word_filter = State()

    add_postfix = State()
    delete_postfix = State()


class Mailing(StatesGroup):
    set_mailing_message = State()


class Moderation(StatesGroup):
    change_text = State()
