from aiogram.types import ContentType
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.manager.protocols import MediaAttachment

from tgbot.misc.widgets.dynamic_media import DynamicMedia
from tgbot.states.add_item import AddItem
from tgbot.states.broadcast_dialog import BroadcastSG
from tgbot.handlers.admin.broadcast import broadcasting, input_text
from tgbot.handlers.admin.add_items import (add_item, add_more, cancel, go_back, 
                                            input_description, input_link, input_title_price, 
                                            to_panel, to_view)


async def item_getter(dialog_manager: DialogManager, **kwargs):
    url = dialog_manager.current_context().dialog_data.get('photo_url')
    return {
        'photo_url': MediaAttachment(ContentType.PHOTO, url=url),
        'title': dialog_manager.current_context().dialog_data.get('title'),
        'description': dialog_manager.current_context().dialog_data.get('description'),
        'price': dialog_manager.current_context().dialog_data.get('price'), 
    }


add_item_dialog = Dialog(
    Window(
        Const('🛠 Административная панель\n'
              'Добавление сслыки\n\n'
              '"<b>http://example.com</b>"'),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=to_panel)),
        MessageInput(input_link),
        state=AddItem.link
    ),    
    
    Window(
        Const('🛠 Административная панель\n'
              'Добавление названия и цены\n\n'
              '"<b>title 25</b>"'),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=go_back)),
        MessageInput(input_title_price),
        state=AddItem.title_price
    ),
    
    Window(
        Const(
              '🛠 Административная панель\n'
              'Добавление описания\n\n'
              '"Lorem ipsum..."'),
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        MessageInput(input_description),
        state=AddItem.description
    ),
    
    Window(
        Const(
            '🛠 Административная панель\n'
            'Просмотр результата'),
        Button(Const('🔮 Просмотр'), id='view', on_click=to_view),
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        state=AddItem.result
    ),
    
    Window(
        DynamicMedia(selector='photo_url'),
        Format(
            '📌 <b>Название:</b> {title}\n'
            '📝 <b>Описание:</b>\n{description}\n\n'
            '💵 <b>Цена:</b> {price}₽'),
        Button(Const('➕ Добавить'), id='add', on_click=add_item),
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        getter=item_getter,
        state=AddItem.view
    ),
    
    Window(
        Const('🎉 Товар был успешно добавлен'),
        Button(Const('➕ Добавить еще'), id='add_more', on_click=add_more),
        Button(Const('🛠 В панель'), id='profile', on_click=cancel),
        state=AddItem.finish
    )
)


async def message_getter(dialog_manager: DialogManager, **kwargs):
    return {'text': dialog_manager.current_context().dialog_data.get('text')}
    
    
broadcast_dialog= Dialog(
    Window(
        Const('🛠 Административная панель\n'
              'Рассылка\n\n'
              'Напишите сообщение которое хотите разослать всем пользователям'),
        MessageInput(input_text),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=to_panel)),
        state=BroadcastSG.message
    ),   
     
    Window(
        Format('🛠 Административная панель\n'
               'Рассылка. Ваше сообщение\n\n'
               '{text}'),
        Row(Button(Const('⬅️ Назад'), id='back', on_click=go_back),
            Button(Const('✍️ Отправить'), id='send', on_click=broadcasting)),
        state=BroadcastSG.confirm,
        getter=message_getter
    )
)


def setup(registry: DialogRegistry):
    registry.register(add_item_dialog)
    registry.register(broadcast_dialog)