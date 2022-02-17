from aiogram import Dispatcher

from .private import enter_ref, info, start, profile, check_allow, plug
from .private.inline_mode import items, show_item, buy_item
from .admin import admin, add_items, del_items


def setup(dp: Dispatcher):
    for module in (admin, items, show_item, buy_item,
                   enter_ref, info, profile, check_allow, 
                   del_items, start, add_items):
        module.setup(dp)