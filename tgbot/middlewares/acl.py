from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import User


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, tg_user: types.User):
        session: AsyncSession = data.get('session')
        user = await session.get(User, tg_user.id)
        if user is None:
            user = User(user_id=tg_user.id, full_name=tg_user.full_name)
            await session.merge(user)
            await session.commit()
        data['user'] = user
        
        
    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.setup_chat(data, call.from_user)