import sqlalchemy as sa
from typing import List

from database.models import Message
from database.session import async_session
from schemas import MessageNotFoundException


class MessageDAL:

    @staticmethod
    async def create(chat_id: int):
        async with async_session() as session, session.begin():
            q = sa.insert(Message).values(chat_id=chat_id).returning(Message.id)

            message_id = (await session.execute(q)).scalar()
            return message_id

    @staticmethod
    async def update(chat_id: int, msg_ids: List[int]):
        async with async_session() as session, session.begin():
            q = sa.select(Message.msg_ids).where(Message.chat_id == chat_id)
            _msg_ids = (await session.execute(q)).scalar()

            if _msg_ids is None:
                raise MessageNotFoundException

            for msg_id in msg_ids:
                _msg_ids.append(msg_id)

            q1 = (
                sa.update(Message)
                .where(Message.chat_id == chat_id)
                .values(msg_ids=_msg_ids)
            )

            await session.execute(q1)

    @staticmethod
    async def get(chat_id: int):
        async with async_session() as session, session.begin():
            q = sa.select(Message.msg_ids).where(Message.chat_id == chat_id)
            _msg_ids = (await session.execute(q)).scalar()

            return _msg_ids

    @staticmethod
    async def clear(chat_id: int):
        async with async_session() as session, session.begin():
            q = sa.update(Message).where(Message.chat_id == chat_id).values(msg_ids=[])

            await session.execute(q)
