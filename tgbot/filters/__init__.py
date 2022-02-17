from aiogram import Dispatcher

from .admin import AdminFilter 


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)