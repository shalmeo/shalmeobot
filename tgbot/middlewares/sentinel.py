from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from tgbot.config import Config
from tgbot.handlers.private.start import start_for_new

from tgbot.services.database.models import User
from tgbot.misc.subscriber import check_subscription


class Sentinel(BaseMiddleware):
    allowed_updates = ["callback_query", "message"]

    async def trigger(self, action, arg):
        obj, *args, data = arg

        if not any(
                update in action for update in self.allowed_updates
        ):
            return

        if not action.startswith("process_"):
            return
        handler = current_handler.get()
        if not handler:
            return

        allow = getattr(handler, "allow", False)
        if allow:
            return

        user: User = data.get("user")
        config: Config = data.get("config")
        
        if user.user_id in config.tg_bot.admin_ids:
            return
        
        subscription = await check_subscription(user_id=user.user_id)
        
        if not (user.referal or subscription):
            await start_for_new(obj)
            raise CancelHandler()