from aiogram.dispatcher.filters.state import StatesGroup, State


class EmailSG(StatesGroup):
    email = State()
    confirm = State()
    finish = State()