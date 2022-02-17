from typing import Dict, Any

from aiogram.types.base import TelegramObject
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from glQiwiApi import QiwiP2PClient



class QiwiWalletMiddleware(LifetimeControllerMiddleware):
    def __init__(self, qiwi_p2p_client: QiwiP2PClient):
        super().__init__()
        self._qiwi_p2p_client = qiwi_p2p_client
        
    
    async def pre_process(self, obj: TelegramObject, data: Dict[str, Any], *args: Any) -> None:
        data["qiwi_p2p_client"] = self._qiwi_p2p_client