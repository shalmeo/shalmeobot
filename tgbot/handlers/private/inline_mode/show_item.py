import re

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.services.database.models import Items
from tgbot.keyboards.inline import buy_kb, del_item_kb


async def show_item(message: types.Message, session: AsyncSession, state: FSMContext, config: Config):
    deep_link = message.get_args()
    item_id = int(deep_link[4:])
    item: Items = await session.get(Items, item_id)
    
    await message.answer_photo(photo=item.photo_url, 
                               caption=f'📌 <b>Артикль:</b> {item.id}\n'
                                       f'📝 <b>Описание:</b>\n{item.description}\n\n'
                                       f'💵 <b>Цена:</b> {item.price}₽', 
                               reply_markup=buy_kb() if message.from_user.id not in config.tg_bot.admin_ids \
                                                     else del_item_kb())
    await state.update_data(item_id=item.id)

def setup(dp: Dispatcher):
    dp.register_message_handler(show_item, CommandStart(deep_link=re.compile(r'^buy_\d{1,}$')))