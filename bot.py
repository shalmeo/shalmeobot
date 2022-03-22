import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from glQiwiApi import QiwiWrapper

from tgbot.config import load_config
from tgbot.services.database.base import Base
from tgbot.misc.set_bot_commands import set_dafault_commands
from tgbot.services.database.utils import get_connection_string
from tgbot import dialogs, middlewares, filters, handlers


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )   
    logger.info("Starting bot")
    config = load_config(".env")
    
    # Creating DB engine for PostgreSQL
    engine = create_async_engine(
        get_connection_string(config.db),
        query_cache_size=1200,
        pool_size=100,
        max_overflow=200,
        future=True,
    )
    
 
    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    # Creating
    storage = RedisStorage2(host='redis') if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    
    wallet = QiwiWrapper(secret_p2p=config.qiwi.p2p_token)
    registry = DialogRegistry(dp)  
    
    # setup
    middlewares.setup(dp, config, db_pool, wallet)
    filters.setup(dp)
    handlers.setup(dp)
    dialogs.setup(registry)

    # set commands
    await set_dafault_commands(bot)
        
    # start
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): 
        logger.error("Bot stopped!")