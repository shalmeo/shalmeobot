from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput


from tgbot.states.email_dialog import EmailSG
from tgbot.handlers.private.info import confirm_email, go_back, input_email


async def email_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'email': dialog_manager.current_context().dialog_data.get('email')
    }


email_dialog = Dialog(
    Window(
        Const('📧 Введите вашу почту'),
        Cancel(Const('Отмена')), 
        MessageInput(input_email),
        state=EmailSG.email
    ),   
    
    Window(
        Format('📧 Вы ввели <b>{email}</b>\n'
               'Чтобы подтвердить нажмите подтвердить.'),
        Button(Const('Подтвердить'), id='confirm', on_click=confirm_email), 
        Button(Const('⬅️ Назад'), id='back', on_click=go_back),
        state=EmailSG.confirm,
        getter=email_getter
    ),
    
    Window(
        Const('🎉 Успешно!\n'
              'Чтобы изменить почту:\n'
              'Информация -> Изменить почту'),
        state=EmailSG.finish
    )
)


def setup(registry: DialogRegistry):
    registry.register(email_dialog)