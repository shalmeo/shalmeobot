from aiogram.dispatcher.filters.state import StatesGroup, State

class AddItem(StatesGroup):
    link = State()
    title_price = State()
    description = State()
    result = State()
    view = State()
    finish = State()