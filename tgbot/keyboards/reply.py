from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_kb():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='✅ Да'), KeyboardButton(text='❌ Нет')]
    ], resize_keyboard=True)
    
    return keyboard


def cancel_kb():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отменить')]
    ], resize_keyboard=True)
    
    return keyboard


def menu_kb():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🏠 Профиль'), KeyboardButton(text='📎 Информация')]
    ], resize_keyboard=True)
    
    return keyboard