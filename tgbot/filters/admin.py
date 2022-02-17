from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'
    is_admin: bool
    
    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        data = ctx_data.get()
        config: Config = data['config']
        return message.from_user.id in config.tg_bot.admin_ids