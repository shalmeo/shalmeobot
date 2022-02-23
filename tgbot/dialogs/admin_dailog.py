from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


from tgbot.handlers.private.plug import plug
from tgbot.handlers.admin.add_items import to_add_item
from tgbot.handlers.admin.admin import admin_panel, go_back
from tgbot.handlers.admin.broadcast import to_broadcast
from tgbot.misc.widgets.switch_current_chat import SwitchCurrentChat
from tgbot.services.database.models import User
from tgbot.states.admin_dialog import AdminSG


async def info_getter(dialog_manager: DialogManager, **kwargs):
    user: User = dialog_manager.data.get('user')
    session: AsyncSession = dialog_manager.data.get('session')
    count_users = await session.scalar(select(func.count(User.user_id)))
    
    return {
        "tg_id": user.user_id,
        'count_users': count_users
    }
    

admin_dialog = Dialog(
    Window(
        Format('<b>Ваш ID:</b> <code>{tg_id}</code>\n'
               '<b>Администратор</b>\n\n'
               '🔎 Статистика\n'
               '└ Кол-во пользователей в базе: <code>{count_users}</code>\n'),
        SwitchCurrentChat(Const('🛒 Каталог')),
        Button(Const('🛠 Админ панель'), id='panel', on_click=admin_panel),
        MessageInput(plug),
        state=AdminSG.main,
        getter=info_getter,
    ),
    
    Window(
        Const('🛠 Административная панель'),
        Button(Const('➕ Добавить товар'), id='add', on_click=to_add_item),
        Button(Const('📣 Рассылка'), id='distribution', on_click=to_broadcast),
        Button(Const('⬅️ Назад'), id='back2', on_click=go_back),
        state=AdminSG.panel
    ),
)


def setup(registry: DialogRegistry):
    registry.register(admin_dialog)
