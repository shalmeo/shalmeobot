from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminSG(StatesGroup):
    main = State()
    panel = State()