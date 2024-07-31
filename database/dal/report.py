import datetime
import sqlalchemy as sa
from typing import List

from database.models.report import Report
from database.session import async_session
from schemas import ReportSchema, ReportNotFoundException


class ReportDAL:

    @staticmethod
    async def create(
        title: str,
        employee_id: int,
        facility_id: int,
        shift_start: datetime,
    ) -> int:
        async with async_session() as session, session.begin():
            q = (
                sa.insert(Report)
                .values(
                    {
                        Report.title: title,
                        Report.employee_id: employee_id,
                        Report.facility_id: facility_id,
                        Report.shift_start: shift_start,
                    }
                )
                .returning(Report.id)
            )

            report_id = (await session.execute(q)).scalar()

            return report_id

    @staticmethod
    async def update_shift_end(id: int, shift_end: datetime):
        async with async_session() as session, session.begin():
            q0 = sa.select(Report.id).where(Report.id == id)
            report_id = (await session.execute(q0)).scalar()

            if not report_id:
                raise ReportNotFoundException

            q = sa.update(Report).where(Report.id == id).values(shift_end=shift_end)

            await session.execute(q)

    @staticmethod
    async def update_description(id: int, description: str):
        async with async_session() as session, session.begin():
            q0 = sa.select(Report.id).where(Report.id == id)
            report_id = (await session.execute(q0)).scalar()

            if not report_id:
                raise ReportNotFoundException

            q = sa.update(Report).where(Report.id == id).values(description=description)

            await session.execute(q)

    @staticmethod
    async def get(id: int) -> ReportSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Report.__table__).where(Report.id == id)
            report = (await session.execute(q)).mappings().first()

            if report:
                return ReportSchema(**report)

    @staticmethod
    async def get_active(employee_id: int) -> ReportSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Report.__table__).where(
                Report.employee_id == employee_id, Report.shift_end == None
            )
            report = (await session.execute(q)).mappings().first()
            if report:
                return ReportSchema(**report)

    @staticmethod
    async def get_by_employee_id(employee_id: int) -> List[ReportSchema]:
        async with async_session() as session, session.begin():
            q = (
                sa.select(Report.__table__)
                .order_by(Report.shift_start)
                .where(Report.employee_id == employee_id)
            )
            reports = (await session.execute(q)).mappings().all()
        return [ReportSchema(**report) for report in reports]

    @staticmethod
    async def get_by_facility_id(facility_id: int) -> List[ReportSchema]:
        async with async_session() as session, session.begin():
            q = (
                sa.select(Report.__table__)
                .order_by(Report.shift_start)
                .where(Report.facility_id == facility_id)
            )

            reports = (await session.execute(q)).mappings().all()
        return [ReportSchema(**report) for report in reports]
