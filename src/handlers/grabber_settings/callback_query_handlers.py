from src.config import dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from src.services.database_service import db_service
from src.helpers import states
from src.utils import keyboards
from src.helpers import filters


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'grabber',
                                   state='*')
async def grabber_settings_handler(msg: CallbackQuery, state: FSMContext):
    await state.finish()

    await msg.message.edit_text(text=db_service.get_grabber_menu(msg.from_user.id),
                                reply_markup=keyboards.grabber)


@dispatcher.callback_query_handler(lambda msg: msg.data == 'source_params')
async def source_params_handler(msg: CallbackQuery, state: FSMContext):
    answer = ('⚙️ Параметры источников\n\n'
              'Нажимая на источник он переключает режимы:\n'
              '🟢 - Модерация\n'
              '🔴 - Не модерируется\n'
              '⚫️ - Отключён')
    await msg.message.edit_text(text=answer,
                                reply_markup=db_service.get_sources_params_reply_markup(msg.from_user.id))


@dispatcher.callback_query_handler(lambda msg: msg.data.startswith('change_moderated_'))
async def change_moderated_handler(msg: CallbackQuery):
    chanel_id = msg.data.split('change_moderated_')[1]
    db_service.change_moderated_status(chanel_id)

    await msg.message.edit_reply_markup(reply_markup=db_service.get_sources_params_reply_markup(msg.from_user.id))


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'grabber_settings',
                                   state='*')
async def grabber_settings_handler(msg: CallbackQuery, state: FSMContext):
    await state.finish()
    await msg.message.edit_text(text='⚙️ Настройки граббера', reply_markup=keyboards.grabber_settings)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'sources')
async def grabber_settings_handler(msg: CallbackQuery):
    await msg.message.edit_text(text=db_service.get_sources_menu(msg.from_user.id),
                                reply_markup=keyboards.sources)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'postfix')
async def grabber_settings_handler(msg: CallbackQuery):
    await msg.message.edit_text(text=db_service.get_postfix_menu(msg.from_user.id),
                                reply_markup=keyboards.postfix)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'add_source')
async def add_source_handler(msg: CallbackQuery):
    await states.GrabberSettings.add_source.set()

    answer = '🔗 Отправь ссылку на канал'
    await msg.message.edit_text(text=answer)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'delete_source')
async def delete_source_handler(msg: CallbackQuery):
    answer = '🗑️ Выбери источник для удаления'
    await msg.message.edit_text(text=answer,
                                reply_markup=db_service.get_sources_reply_markup(msg.from_user.id))

    await states.GrabberSettings.delete_source.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   state=states.GrabberSettings.delete_source)
async def delete_source_handler(msg: CallbackQuery, state: FSMContext):
    answer = '✅️ Источник удалён'
    db_service.delete_source(msg.data)
    await msg.answer(text=answer)

    await msg.message.edit_text(text=db_service.get_sources_menu(msg.from_user.id),
                                reply_markup=keyboards.sources)
    await state.finish()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'words_filters', state='*')
async def words_filters_handler(msg: CallbackQuery, state: FSMContext):
    await state.finish()
    answer = db_service.get_words_filters_menu(msg.from_user.id)

    await msg.message.edit_text(text=answer, reply_markup=keyboards.words_filters)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'add_stop_word')
async def add_stop_word_handler(msg: CallbackQuery):
    answer = '🚀 Отправь стоп-слово'
    await msg.message.edit_text(text=answer)

    await states.GrabberSettings.add_stop_word.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'delete_stop_word')
async def delete_stop_word_handler(msg: CallbackQuery):
    answer = '🗑️ Выбери стоп-слово для удаления'
    await msg.message.edit_text(text=answer,
                                reply_markup=db_service.get_stop_words_reply_markup(msg.from_user.id))

    await states.GrabberSettings.delete_stop_word.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   state=states.GrabberSettings.delete_stop_word)
async def delete_stop_word_handler(msg: CallbackQuery, state: FSMContext):
    answer = '✅️ Стоп-слово удалено'
    db_service.delete_stop_word(msg.data)
    await msg.answer(text=answer)

    await msg.message.edit_text(text=db_service.get_words_filters_menu(msg.from_user.id),
                                reply_markup=keyboards.words_filters)
    await state.finish()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'add_word_filter')
async def add_word_filter_handler(msg: CallbackQuery):
    answer = '🚀 Отправь фильтр-слово'
    await msg.message.edit_text(text=answer)

    await states.GrabberSettings.add_filter_filtered_word.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'delete_word_filter')
async def delete_word_filter_handler(msg: CallbackQuery):
    answer = '🗑️ Выбери фильтр для удаления'
    await msg.message.edit_text(text=answer,
                                reply_markup=db_service.get_words_filters_reply_markup(msg.from_user.id))

    await states.GrabberSettings.delete_word_filter.set()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   state=states.GrabberSettings.delete_word_filter)
async def delete_word_filter_handler(msg: CallbackQuery, state: FSMContext):
    answer = '✅️ Фильтр удалён'
    db_service.delete_word_filter(msg.data)
    await msg.answer(text=answer)

    await msg.message.edit_text(text=db_service.get_words_filters_menu(msg.from_user.id),
                                reply_markup=keyboards.words_filters)
    await state.finish()


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'set_postfix',
                                   state='*')
async def add_postfix_handler(msg: CallbackQuery):
    await states.GrabberSettings.add_postfix.set()

    answer = '🚀 Отправь новый постфикс'
    await msg.message.edit_text(text=answer)


@dispatcher.callback_query_handler(filters.UserIsChannelSubscriber(),
                                   filters.UserWithSubscribe(),
                                   lambda msg: msg.data == 'delete_postfix')
async def delete_postfix(msg: CallbackQuery):
    answer = '🗑️ Постфикс удалён'
    await msg.answer(text=answer)

    answer = db_service.delete_postfix(msg.from_user.id)

    await msg.message.edit_text(text=answer,
                                reply_markup=db_service.get_sources_reply_markup(msg.from_user.id))

    await states.GrabberSettings.delete_postfix.set()
