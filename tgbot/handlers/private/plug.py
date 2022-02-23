from aiogram import types
from aiogram_dialog import Dialog, DialogManager


async def plug(message: types.Message, dialog: Dialog, manager: DialogManager):
    await manager.reset_stack()
