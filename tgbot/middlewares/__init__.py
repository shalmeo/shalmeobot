from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .config import ConfigMiddleware
from .db import DbSessionMiddleware
from .acl import ACLMiddleware
from .sentinel import Sentinel
from .qiwi_wallet import QiwiWalletMiddleware

def setup(dp: Dispatcher, config, db_pool, wallet):
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(DbSessionMiddleware(db_pool))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(Sentinel())
    dp.setup_middleware(ConfigMiddleware(config))
    dp.setup_middleware(QiwiWalletMiddleware(wallet))