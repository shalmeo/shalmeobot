from aiogram import types, Dispatcher

from tgbot.services.database.models import User
from . start import user_start
from tgbot.misc.allow_acc import allow_acces
from tgbot.misc.subscriber import check_subscription


@allow_acces()
async def check_allow(call: types.CallbackQuery, user: User):
    
    subscription = await check_subscription(user_id=user.user_id)
    
    if user.referal or subscription:
        await call.message.delete()
        await user_start(call.message)
    else:
        await call.answer('Доступ к боту запрещен! 🚫', show_alert=False)

def setup(dp: Dispatcher):
    dp.register_callback_query_handler(check_allow, text='check_allow')