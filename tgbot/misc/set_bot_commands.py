from aiogram import Bot, types


async def set_dafault_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand('start', 'Старт')
    ])