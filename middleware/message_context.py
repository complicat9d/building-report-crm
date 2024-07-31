from typing import List

from bot import bot
from database.dal import MessageDAL


class MessageContext:

    @staticmethod
    async def update(chat_id: int, msg_ids: List[int]):
        await MessageDAL.update(chat_id, msg_ids)

    @staticmethod
    async def clear(chat_id: int):
        _msg_ids = await MessageDAL.get(chat_id)
        for msg_id in _msg_ids:
            try:
                await bot.delete_message(chat_id, msg_id)
            except Exception:
                # 48 hours have passed and message cannot be deleted due to telegram api restrictions
                pass

        await MessageDAL.clear(chat_id)
