from aiogram.dispatcher.filters.state import StatesGroup, State


class BroadcastSG(StatesGroup):
    message = State()
    confirm = State()