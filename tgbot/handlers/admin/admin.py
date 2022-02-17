from aiogram import types, Dispatcher
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.states.admin_dialog import AdminSG


async def admin(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.main)


async def admin_panel(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AdminSG.panel)


async def go_back(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AdminSG.main)


def setup(dp: Dispatcher):
    dp.register_message_handler(admin, text='🏠 Профиль', state='*', is_admin=True)