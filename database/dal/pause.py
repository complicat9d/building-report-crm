import sqlalchemy as sa
from typing import List
from datetime import datetime, timedelta

from database.models import Pause
from database.session import async_session
from schemas import PauseSchema, PauseNotFoundException


class PauseDAL:

    @staticmethod
    async def create(start: datetime, report_id: int) -> int:
        async with async_session() as session, session.begin():
            q = (
                sa.insert(Pause)
                .values({Pause.start: start, Pause.report_id: report_id})
                .returning(Pause.id)
            )

            pause_id = (await session.execute(q)).scalar()

            return pause_id

    @staticmethod
    async def update(id: int, end: datetime):
        async with async_session() as session, session.begin():
            q0 = sa.select(Pause.id).where(Pause.id == id)
            pause_id = (await session.execute(q0)).scalar()

            if not pause_id:
                raise PauseNotFoundException

            q = sa.update(Pause).where(Pause.id == id).values(end=end)
            await session.execute(q)

    @staticmethod
    async def get_active(report_id: int) -> PauseSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Pause.__table__).where(
                Pause.report_id == report_id, Pause.end == None
            )
            pause = (await session.execute(q)).mappings().first()
            if pause:
                return Pause(**pause)

    @staticmethod
    async def get_by_report_id(report_id: int) -> List[PauseSchema]:
        async with async_session() as session, session.begin():
            q = sa.select(Pause.__table__).where(Pause.report_id == report_id)
            pauses = (await session.execute(q)).mappings().all()
            return [PauseSchema(**pause) for pause in pauses]

    @staticmethod
    async def get_break_time(report_id: int):
        async with async_session() as session, session.begin():
            q = sa.select(Pause.start, Pause.end).where(
                Pause.report_id == report_id, Pause.end != None
            )
            intervals = (await session.execute(q)).fetchall()
            return sum([(end - start) for start, end in intervals], start=timedelta())
