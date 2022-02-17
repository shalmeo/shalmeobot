from aiogram import types, Dispatcher
from aiogram_dialog import DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import Items
from tgbot.states.add_item import AddItem
from tgbot.states.admin_dialog import AdminSG


async def to_add_item(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AddItem.link)


async def input_link(message: types.Message, dialog: Dialog, manager: DialogManager):
    if message.entities[0]['type'] == 'url':
        manager.current_context().dialog_data["photo_url"] = message.text
        await dialog.next()
    else:
        await message.answer('Фото должно быть ссылкой')
    

async def input_title_price(message: types.Message, dialog: Dialog, manager: DialogManager):
    *title, price = message.text.split()
    if price.isdigit():
        manager.current_context().dialog_data["title"] = ' '.join(title)
        manager.current_context().dialog_data["price"] = int(price)
        await dialog.next()
    else: 
        await message.answer('Цена должна быть целым числом')


async def input_description(message: types.Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["description"] = message.text
    await dialog.next()
    
    
async def to_view(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AddItem.view)
    
    
async def add_item(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.data.get('session')
    
    data = dialog_manager.current_context().dialog_data
    await session.merge(Items(**data))
    await session.commit()
    
    await dialog_manager.switch_to(AddItem.finish)
    
    
async def add_more(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AddItem.link) 
        

async def cancel(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.panel)
        
        
async def go_back(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().back()
    
    
async def to_panel(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(AdminSG.panel)
    
    
def setup(dp: Dispatcher):
    pass