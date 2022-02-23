import asyncio
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.inline import info_kb
from tgbot.misc.throttling import rate_limit
from tgbot.services.database.models import User
from tgbot.states.email_dialog import EmailSG


@rate_limit(limit=2)
async def show_info(message: types.Message, session: AsyncSession):
    user: User = await session.get(User, message.from_user.id)
    await message.answer('1.1 Чтобы пользоваться нашим сервисом вам необходимо привязать вашу почту. После привязки вы сможете делать покупки. Ваша почта нужна нам для того, чтобы мы с вами связались после того как вы совершите покупку.\n\n'
                         '1.2 Massa tempor nec feugiat nisl pretium. Integer malesuada nunc vel risus. Dui id ornare arcu odio. Vitae congue eu consequat ac felis donec. Enim neque volutpat ac tincidunt vitae semper quis. Ultricies integer quis auctor elit sed vulputate mi sit amet.\n\n\n'
                         '2.1 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Aliquam ultrices sagittis orci a scelerisque purus semper eget. At quis risus sed vulputate odio ut enim.\n\n'
                         '2.2 Enim eu turpis egestas pretium. Orci sagittis eu volutpat odio facilisis mauris. Commodo sed egestas egestas fringilla. Scelerisque purus semper eget duis at tellus at urna condimentum.',
                         reply_markup=info_kb(user.email))
    

async def bind_email(call: types.CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(EmailSG.email, mode=StartMode.RESET_STACK)


async def input_email(message: types.Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["email"] = message.text
    await dialog.next()
    
    
async def confirm_email(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await call.message.answer('🎉 Успешно!\n'
                              'Чтобы изменить почту:\n'
                              'Информация -> Изменить почту')
    
    session: AsyncSession = dialog_manager.data.get('session')
    email = dialog_manager.current_context().dialog_data.get('email')
    await session.execute(update(User).where(User.user_id == call.from_user.id).values(email=email))
    await session.commit()


async def go_back(call: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.dialog().back()
   
   
async def close_info(call: types.CallbackQuery, state: FSMContext):
    message = call.message.message_id - 1
    await call.message.delete()
    await call.bot.delete_message(call.from_user.id, message)

    
def setup(dp: Dispatcher):
    dp.register_message_handler(show_info, text='📎 Информация')
    dp.register_callback_query_handler(bind_email, text='bind_email')
    dp.register_callback_query_handler(close_info, text='close_info')