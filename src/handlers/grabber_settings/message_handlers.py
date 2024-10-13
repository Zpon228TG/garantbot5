from src.config import dispatcher, scheduler
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from src.utils import keyboards
from src.config import config
from src.helpers.sqlalchemy_models import SourceChannel
from src.services.database_service import db_service
from src.helpers.scheduler_jobs import check_channels_task
from src.helpers import states, filters


def run_check_channel_tasks():
    scheduler.add_job(check_channels_task, 'interval', seconds=config.SCHEDULER_TASKS_INTERVAL)
    scheduler.start()
    print('> All tasks running')


run_check_channel_tasks()


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.GrabberSettings.add_source)
async def add_source_handler(msg: Message, state: FSMContext):
    channel_id, channel_name = await db_service.add_source(msg.from_user.id, msg.text)

    answer = (f'✅ Новые записи будут канала <b>{channel_name}</b> отслеживаться\n\n'
              f'❗️ Вы должны сделать этого бота администратором в вашем канале')
    await msg.answer(text=answer)

    await state.finish()


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.GrabberSettings.add_stop_word)
async def grabber_settings_handler(msg: Message, state: FSMContext):
    answer = db_service.add_stop_word(msg.from_user.id, msg.text)

    await msg.answer(text=answer,
                     reply_markup=keyboards.words_filters)

    await state.finish()


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.GrabberSettings.add_filter_filtered_word)
async def add_word_filter_handler(msg: Message, state: FSMContext):
    answer = '🚀 Отправь слово, на которое бот будет заменять'
    await msg.answer(text=answer)

    state_data = {
        'filtered_word': msg.text
    }
    await state.update_data(state_data)

    await states.GrabberSettings.add_filter_substituted_word.set()


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.GrabberSettings.add_filter_substituted_word)
async def add_word_filter_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    filtered_word = state_data.get('filtered_word')
    answer = db_service.add_word_filter(msg.from_user.id, filtered_word, msg.html_text)
    await msg.answer(text=answer,
                     reply_markup=keyboards.words_filters)

    await state.finish()


@dispatcher.message_handler(filters.UserIsChannelSubscriber(),
                            filters.UserWithSubscribe(),
                            state=states.GrabberSettings.add_postfix)
async def add_postfix_handler(msg: Message, state: FSMContext):
    await state.finish()

    db_service.add_postfix(msg.from_user.id, msg.html_text)

    answer = '✅ Постфикс установлен'
    await msg.answer(text=answer, reply_markup=keyboards.postfix)
