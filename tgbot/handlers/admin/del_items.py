from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import Items
from tgbot.keyboards.inline import item_cb
from tgbot.services.database.quick_commands import delete_item


async def del_item(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    item_id = (await state.get_data()).get('item_id')
    item: Items = await session.get(Items, item_id)
    result = await delete_item(session, item.id)
    
    if result:
        await call.message.edit_caption('🎉 Товар был успешно удален')
    else:
        await call.answer('😔 Что-то пошло не так', show_alert=False)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(del_item, item_cb.filter(action='del'))