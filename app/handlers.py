from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.middlewares import TestMiddleware

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


