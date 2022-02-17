import asyncio
import logging

from aiogram import Bot
from aiogram.utils import exceptions


async def send_message(bot: Bot, user_id, text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(bot, user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def send_admin(bot, user_mention, admins, item, user):
    text = [f'Пользователь {user_mention} совершил покупку\n\n',
            f'<b>{item.title} {item.price}₽\n',
            f'Почта: {user.email}</b>']
    count = 0
    try:
        for admin in admins:
            if await send_message(bot, admin, ''.join(text)):
                count += 1
            await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")