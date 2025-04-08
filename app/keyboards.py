from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Category')],
    [KeyboardButton(text='Trash'), KeyboardButton(text='Contacts')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose you destiny!'
)


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Catalog", callback_data='catalog')],
    [InlineKeyboardButton(text='Basket', callback_data='basket'), InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])


cars = ['Tesla', 'Mercedes', 'BMW']

async def reply_button_cars():
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(2).as_markup()


async def inline_button_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url="https://pranx.com/hacker/"))
    return keyboard.adjust(2).as_markup()



