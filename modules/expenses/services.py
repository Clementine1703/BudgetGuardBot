from typing import Union

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON
from core.utils import send_validation_error_report
from . import states, stages, repositories
from .schemas import ExpenseValidator


async def handle_select_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос выбора категории расхода.

    Загружает список всех категорий пользователя, формирует кнопки с этими категориями,
    добавляет кнопку создания новой категории и кнопку возврата в главное меню.
    Обновляет сообщение с текстом и клавиатурой выбора категории.
    Устанавливает состояние FSM в выбор категории.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    keyboard = await get_categories_kb(cb.from_user.id)
    await cb.message.edit_text(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddExpense.select_category)


async def handle_create_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос на создание новой категории расхода.

    Отправляет сообщение с приглашением ввести название новой категории
    и обновляет состояние FSM на ввод создания категории.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    await cb.message.edit_text(
        stages.CATEGORY_CREATION.msg(),
        reply_markup=stages.CATEGORY_CREATION.kb()
    )
    await state.set_state(states.AddExpense.create_category)


async def handle_select_deleting_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос на выбор категории для удаления расхода.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    keyboard = await get_categories_kb(cb.from_user.id, simplified=True)
    await cb.message.edit_text(
        stages.DELETE_CATEGORY_SELECTION.msg(),
        reply_markup=stages.DELETE_CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddExpense.delete_category)


async def handle_delete_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Удаляет категорию расхода.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    category_id = int(cb.data.split(':')[-1])
    await repositories.delete_category(cb.from_user.id, category_id)
    keyboard = await get_categories_kb(cb.from_user.id)
    await cb.message.edit_text(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddExpense.select_category)


async def handle_input_new_category(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод пользователем названия новой категории.

    Валидирует введённое название, если валидно — сохраняет категорию в базу,
    обновляет клавиатуру выбора категории, отправляет сообщение с обновлённым списком
    и переключает состояние FSM обратно на выбор категории.
    В случае ошибки валидации — отправляет отчёт об ошибке.

    Args:
        message (Message): входящее сообщение от пользователя с названием категории.
        state (FSMContext): контекст состояния FSM.
    """
    try:
        ExpenseValidator(category=message.text)
    except ValidationError as e:
        await send_validation_error_report(message, e)
        return

    await repositories.create_category(message.from_user.id, message.text)

    keyboard = await get_categories_kb(message.from_user.id)
    await message.answer(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddExpense.select_category)


async def handle_input_amount(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает выбор категории и переход к вводу суммы расхода.

    Извлекает id выбранной категории из callback данных,
    сохраняет в состояние FSM и отправляет сообщение с приглашением ввести сумму,
    устанавливает соответствующее состояние FSM.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    category_id = cb.data.split(':')[-1]
    await state.clear()
    await state.update_data(category_id=int(category_id))

    await cb.message.edit_text(
        stages.AMOUNT_INPUT.msg(),
        reply_markup=stages.AMOUNT_INPUT.kb()
    )
    await state.set_state(states.AddExpense.input_amount)


async def handle_input_comment(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод суммы расхода пользователем.

    Валидирует сумму, сохраняет её в состояние FSM,
    отправляет сообщение с приглашением ввести комментарий,
    переключает FSM на состояние ввода комментария.
    В случае ошибки валидации — отправляет отчёт об ошибке.

    Args:
        message (Message): входящее сообщение с суммой.
        state (FSMContext): контекст состояния FSM.
    """
    try:
        ExpenseValidator(amount=message.text)
    except ValidationError as e:
        await send_validation_error_report(message, e)
        return

    amount = message.text
    await state.update_data(amount=int(amount))
    await message.answer(
        stages.COMMENT_INPUT.msg(),
        reply_markup=stages.COMMENT_INPUT.kb()
    )
    await state.set_state(states.AddExpense.input_comment)


async def handle_addition_expense(event: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
    Завершает добавление расхода.

    Обрабатывает комментарий, если он пришёл сообщением,
    валидирует комментарий и сохраняет в состояние FSM.
    Создаёт запись расхода в базе данных из собранных данных FSM.
    Обновляет клавиатуру выбора категории,
    отправляет сообщение об успешном добавлении и переключает FSM на выбор категории.

    Args:
        event (Union[Message, CallbackQuery]): сообщение или callback, инициирующий добавление.
        state (FSMContext): контекст состояния FSM.
    """
    if isinstance(event, Message):
        try:
            ExpenseValidator(comment=event.text)
        except ValidationError as e:
            await send_validation_error_report(event, e)
            return

        comment = event.text
        await state.update_data(comment=comment)
        message = event
    else:
        message = event.message


    expense_data = await state.get_data()
    await repositories.create_expense(expense_data)

    keyboard = await get_categories_kb(message.from_user.id)
    await message.answer(
        f'Расход успешно добавлен\n\n{stages.CATEGORY_SELECTION.msg()}',
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddExpense.select_category)


async def get_categories_kb(user_id: int, simplified: bool = False) -> list[list[tuple[str, str] | InlineKeyboardButton]]:
    categories = await repositories.get_all_categories(user_id)
    buttons = [[(c.name, f'{Callbacks.EXPENSE.ADD_AMOUNT}:{str(c.id)}')] for c in categories]
    buttons.extend([
            [MAIN_MENU_BUTTON]
        ] if simplified else [
            [("➕ Создать категорию расходов", Callbacks.EXPENSE.CREATE_CATEGORY)],
            [("❌ Удалить категорию расходов", Callbacks.EXPENSE.DELETE_CATEGORY)],
            [MAIN_MENU_BUTTON],
        ]
    )
    return buttons
