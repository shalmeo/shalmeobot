from aiogram.dispatcher.filters.state import StatesGroup, State

class EnterReferal(StatesGroup):
    enter = State()
    confirm = State()