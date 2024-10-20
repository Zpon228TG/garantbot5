from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.inline_user import user_payments_kb, user_payment_kb
from tgbot.utils.const_functions import is_number


router = Router(name=__name__)


# Класс состояний.
class States(StatesGroup):
    get_sum = State()
    check_pay = State()


# Обработчик кнопки "💰 Пополнить".
@router.callback_query(F.data == "user_refill")
async def send_payments(callback: CallbackQuery) -> None:
    """Асинхронный обработчик нажатия кнопки "💰 Пополнить".\n
    Принимает в себя в качестве аргументов объект класса CallbackQuery.\n
    Удаляет предыдущее сообщение и присылает пользователю список с выбором платежной
    системы для пополнения баланса и соответствующее сообщение.\n\n """

    await callback.message.delete()

    await callback.message.answer(
        text="<b>🖲 Выберите способы пополнений</b>",
        reply_markup=user_payments_kb(),
    )


# Обработчик выбора платежной системы.
@router.callback_query(F.data.startswith("user_refill_method:"))
async def select_payment_system(callback: CallbackQuery, state: FSMContext) -> None:
    """Асинхронный обработчик выбора платежной системы.\n
    Принимает в себя в качестве аргументов объекты класса CallbackQuery и FSMContext.\n
    Сохраняет в состоянии FSM информацию о выбранной платежной системе
    и открывает новое состояние FSM: States.get_sum, также присылает соответствующее сообщение.\n\n """

    pay_method = callback.data.split(":")[1]

    await state.update_data(here_pay_method=pay_method)
    await state.set_state(States.get_sum)

    await callback.message.edit_text("<b>💰 Введите сумму пополнения</b>")


# Обработчик выбора суммы к пополнению.
@router.message(F.text, States.get_sum)
async def get_amount(message: Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()

    if is_number(amount):
        if float(amount) > MIN_AMOUNT:
            selected_payment_system = data.get('here_pay_method')
            api_system = payment_systems.get(selected_payment_system)
            payment_link = await api_system.generate_pay_link(amount=float(amount))

            await message.answer(
                text='Для пополнения баланса перейди по ссылке:\n\n' + payment_link,
                reply_markup=user_payment_kb(payment_url=payment_link),
            )
            await state.update_data(api_system=api_system)
            await state.set_state(States.check_pay)
        else:
            await message.answer(
                f"<b>❌ Неверная сумма пополнения</b>\n"
                f"❗️Сумма не должна быть меньше <code>{MIN_AMOUNT}₽</code> и больше <code>100 000₽</code>\n"
                f"💰 Введите сумму для пополнения средств <b>еще раз:</b>",
            )
            await state.set_state(States.get_sum)

    else:
        await message.answer(
            "<b>❌ Данные были введены неверно.</b>\n"
            "💰 Введите сумму для пополнения средств <b>еще раз:</b>",
        )
        await state.set_state(States.get_sum)


# Обработчик нажатия кнопки "Проверить оплату ✅"
@router.callback_query(States.check_pay, F.data == 'check_payment')
async def check_pay(callback: CallbackQuery, state: FSMContext) -> None:
    """Асинхронный обработчик кнопки "Проверить оплату ✅".\n
    В качестве аргументов принимает в себя объекты класса CallbackQuery и FSMContext.\n
    Удаляет предыдущее сообщение и проверяет статус оплаты.
    При совершенно оплате, деньги зачисляются на баланс в профиле игрового магазина и очищается состояние FSM.
    Иначе, присылается предупредительное сообщение и снова открывается состояние FSM.\n\n """

    data = await state.get_data()
    payment_system = data.get('api_system')
    payment_status = await payment_system.get_pay_status()

    if payment_status:
        await callback.message.delete()

        await callback.message.answer(
            text='✅ Отлично! Оплата прошла успешно!\n\n'
                 '💰 Деньги зачислены на баланс. \n'
        )
        user = await MyRequests.get_line('Users', 'user_id', callback.from_user.id,)
        await MyRequests.update_items('Users', 'user_id', callback.from_user.id, balance=float(user.balance) + float(data.get('sum')))

        await send_profile(callback)

    else:
        await callback.message.answer('❌ <b>Оплата не была произведена, скорее пополни баланс!</b>')

        await state.set_state(StatesProfile.check_pay)
