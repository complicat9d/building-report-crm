import sqlalchemy as sa

from database.models import FacilityEmployeeRelationship
from database.session import async_session


class FacilityEmployeeDAL:

    @staticmethod
    async def create(facility_id: int, employee_id: int):
        async with async_session() as session, session.begin():
            q = (
                sa.insert(FacilityEmployeeRelationship)
                .values(
                    {
                        FacilityEmployeeRelationship.facility_id: facility_id,
                        FacilityEmployeeRelationship.employee_id: employee_id,
                    }
                )
                .returning(FacilityEmployeeRelationship.id)
            )

            facility_employee_id = (await session.execute(q)).scalar()

            return facility_employee_id

    @staticmethod
    async def delete(facility_id: int, employee_id: int):
        async with async_session() as session, session.begin():
            q = sa.delete(FacilityEmployeeRelationship).where(
                FacilityEmployeeRelationship.facility_id == facility_id,
                FacilityEmployeeRelationship.employee_id == employee_id,
            )

            await session.execute(q)
