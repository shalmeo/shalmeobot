from aiogram import types
from aiogram_dialog import DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.config import Config

from tgbot.misc.broadcaster import broadcast
from tgbot.services.database.models import User
from tgbot.states.broadcast_dialog import BroadcastSG


async def to_broadcast(call, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(BroadcastSG.message)


async def input_text(message: types.Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["text"] = message.text
    await dialog.next()


async def broadcasting(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await call.message.delete()
    
    session: AsyncSession = dialog_manager.data.get('session')
    config: Config = dialog_manager.data.get('config')
    
    users = await session.scalars(select(User).where(User.user_id.notin_(config.tg_bot.admin_ids)))
    text = dialog_manager.current_context().dialog_data.get('text')
    count = await broadcast(call.bot, users, text)
    
    await call.message.answer(f'Сообщение отправлено {count} пользователям')