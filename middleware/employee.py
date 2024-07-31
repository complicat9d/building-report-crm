from typing import List
import sqlalchemy as sa
from uuid import uuid4

from database.session import async_session
from database.models import Employee, FacilityEmployeeRelationship


class EmployeeMiddleware:

    @staticmethod
    async def create(fio: str, job_title: str = None, facilities: List[int] = None):
        async with async_session() as session, session.begin():
            q = (
                sa.insert(Employee)
                .values(
                    {
                        Employee.fio: fio,
                        Employee.job_title: job_title,
                        Employee.token: uuid4(),
                    }
                )
                .returning(Employee.id)
            )
            employee_id = (await session.execute(q)).scalar()

            if facilities:
                for facility_id in facilities:
                    q1 = sa.insert(FacilityEmployeeRelationship).values(
                        {
                            FacilityEmployeeRelationship.employee_id: employee_id,
                            FacilityEmployeeRelationship.facility_id: facility_id,
                        }
                    )
                    await session.execute(q1)

            return employee_id
