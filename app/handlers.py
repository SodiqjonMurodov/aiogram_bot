from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb

router = Router()


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


