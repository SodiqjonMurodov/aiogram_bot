from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import TestMiddleware
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

import app.keyboards as kb

router = Router()

router.message.middleware(TestMiddleware())
# router.message.outer_middleware(TestMiddleware())


class Reg(StatesGroup):
    """ Registration template statement """
    full_name = State()
    phone_number = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello brother", reply_markup=kb.settings)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(f"This command /help")


@router.message(Command("get_photo"))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://www.marktechpost.com/wp-content/uploads/2023/07/sute-mouse-dj-disco-dancing-generative-ai-scaled.jpg', 
                               caption="Ai photo")
    

@router.message(F.photo)
async def send_photo(message: Message):
    await message.answer(f"ID photo: {message.photo[-1].file_id}")



# Callback handlers
@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text('Hello!')


@router.callback_query(F.data == 'basket')
async def basket(callback: CallbackQuery):
    await callback.answer('You choice basket button')
    await callback.message.answer('Hello mother!')


@router.callback_query(F.data == 'contacts')
async def contacts(callback: CallbackQuery):
    await callback.answer('You choice contacts button', show_alert=True)
    await callback.message.answer('Hello motherf**ker!')

# Registration part
@router.message(Command('reg'))
async def reg_first_step(message: Message, state: FSMContext):
    await state.set_state(Reg.full_name) # set state
    await message.answer('Please, enter your name.')


@router.message(Reg.full_name)
async def reg_second_step(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.phone_number) # change state
    await message.answer('Please, enter your phone number.')


@router.message(Reg.phone_number)
async def reg_third_step(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f'Thank you, registration complited.\nName: {data['full_name']}\nPhone number: {data['phone_number']}')
    await state.clear() # clear statement cache


@router.message(Command("reply_builder"))
async def reply_builder(message: Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )


@router.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    # ... второй из одной ...
    builder.row(types.KeyboardButton(
        text="Создать викторину",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    # ... а третий снова из двух
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    # WebApp-ов пока нет, сорри :(

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@router.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )


@router.message(F.chat_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )

    