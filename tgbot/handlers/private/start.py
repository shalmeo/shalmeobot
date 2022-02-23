import re

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.reply import menu_kb
from tgbot.misc.allow_acc import allow_acces
from tgbot.keyboards.inline import starting_kb
from tgbot.services.database.models import User
from tgbot.services.database.quick_commands import add_referal


async def start_for_new(message: types.Message):
    await message.answer("Привет 👋\n"
                         "Чтобы пользоваться ботом 🤖, тебе нужно выполнить один из этих пунктов:\n\n"
                         "📍 Быть подписанным на наш новостной канал\n"
                         "📍 Быть приглашенным от кого-либо\n"
                         "📍 Ввести код пригасившего", reply_markup=starting_kb())


async def user_start(message: types.Message):
    await message.answer('Вы были перенесены в меню! 🎛', reply_markup=menu_kb())


@allow_acces()
async def user_start_with_deeplink(message: types.Message, session: AsyncSession, user: User):
    if ref := await session.get(User, int(message.get_args())):
        await message.answer('Вы были перенесены в меню! 🎛', reply_markup=menu_kb())
        await add_referal(session=session, ref_id=ref.user_id, user=user)
    else:
        await start_for_new(message)


def setup(dp: Dispatcher):
    dp.register_message_handler(user_start_with_deeplink,
                                CommandStart(deep_link=re.compile(r'^\d{1,}$')),
                                state='*')
    dp.register_message_handler(user_start, commands=["start"], state='*')
