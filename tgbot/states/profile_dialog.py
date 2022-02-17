from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileSG(StatesGroup):
    profile = State()
    referal = State()
    feedback = State()