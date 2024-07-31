import sqlalchemy as sa
from typing import List

from database.models import Facility, FacilityEmployeeRelationship
from database.session import async_session
from schemas import FacilityNotFoundException, FacilitySchema


class FacilityDAL:

    @staticmethod
    async def create(
        title: str,
        description: str,
        active: bool,
        address: str,
        employees: List[int] = None,
    ) -> int:
        async with async_session() as session, session.begin():
            q = (
                sa.insert(Facility)
                .values(
                    {
                        Facility.title: title,
                        Facility.description: description,
                        Facility.active: active,
                        Facility.address: address,
                    }
                )
                .returning(Facility.id)
            )
            facility_id = (await session.execute(q)).scalar()

            if employees:
                for emp in employees:
                    q1 = sa.insert(FacilityEmployeeRelationship).values(
                        {
                            FacilityEmployeeRelationship.facility_id: facility_id,
                            FacilityEmployeeRelationship.employee_id: emp,
                        }
                    )
                    await session.execute(q1)

        return facility_id

    @staticmethod
    async def update(
        id: int,
        title: str = None,
        description: str = None,
        address: str = None,
        active: bool = None,
        employees: List[int] = None,
    ):
        async with async_session() as session, session.begin():
            q0 = sa.select(Facility.id).where(Facility.id == id)
            facility_id: int = (await session.execute(q0)).scalar()

            if not facility_id:
                raise FacilityNotFoundException

            data = {}
            if title:
                data[Facility.title] = title
            if description:
                data[Facility.description] = description
            if address:
                data[Facility.address] = address
            if active is not None:
                data[Facility.active] = active

            q = sa.update(Facility).where(Facility.id == facility_id).values(data)

            await session.execute(q)

            q1 = sa.select(FacilityEmployeeRelationship.id).where(
                FacilityEmployeeRelationship.facility_id == facility_id
            )
            relation_ids = (await session.execute(q1)).scalars().all()
            for relation_id in relation_ids:
                q2 = sa.delete(FacilityEmployeeRelationship).where(
                    FacilityEmployeeRelationship.id == relation_id
                )
                await session.execute(q2)

            for employee_id in employees:
                q3 = sa.insert(FacilityEmployeeRelationship).values(
                    {
                        FacilityEmployeeRelationship.facility_id: facility_id,
                        FacilityEmployeeRelationship.employee_id: employee_id,
                    }
                )
                await session.execute(q3)

    @staticmethod
    async def delete(id: int):
        async with async_session() as session, session.begin():
            q0 = sa.select(Facility.id).where(Facility.id == id)
            facility_id = (await session.execute(q0)).scalar()

            if not facility_id:
                raise FacilityNotFoundException

            q1 = sa.delete(Facility).where(Facility.id == id)

            await session.execute(q1)

    @staticmethod
    async def get(id: int) -> FacilitySchema:
        async with async_session() as session, session.begin():
            q = sa.select(Facility.__table__).where(Facility.id == id)
            facility = (await session.execute(q)).mappings().first()
            if facility:
                return FacilitySchema(**facility)

    @staticmethod
    async def get_all_by_employee_id(employee_id: int) -> List[FacilitySchema]:
        async with async_session() as session, session.begin():
            q = sa.select(Facility.__table__).where(
                sa.and_(
                    FacilityEmployeeRelationship.employee_id == employee_id,
                    Facility.id == FacilityEmployeeRelationship.facility_id,
                )
            )
            facilities = (await session.execute(q)).mappings().all()
            return [FacilitySchema(**facility) for facility in facilities]

    @staticmethod
    async def get_all() -> List[FacilitySchema]:
        async with async_session() as session, session.begin():
            q = sa.select(Facility.__table__)
            facilities = (await session.execute(q)).mappings().all()
            return [FacilitySchema(**facility) for facility in facilities]
