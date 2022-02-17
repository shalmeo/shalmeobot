from typing import List, Callable, Optional, Union, Dict, Any

from aiogram.types import InlineKeyboardButton

from aiogram_dialog.manager.manager import DialogManager
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.kbd import Keyboard


class SwitchCurrentChat(Keyboard):
    def __init__(self, text: Text, id: Optional[str] = None, when: Union[str, Callable, None] = None):
        super().__init__(id, when)
        self.text = text

    async def _render_keyboard(self, data: Dict, manager: DialogManager) -> List[List[InlineKeyboardButton]]:
        return [[
            InlineKeyboardButton(
                text=await self.text.render_text(data, manager),
                switch_inline_query_current_chat=''
            )
        ]]