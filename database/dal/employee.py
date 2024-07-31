import sqlalchemy as sa
from uuid import uuid4, UUID
from typing import List

from database.models import Employee, FacilityEmployeeRelationship
from database.session import async_session
from schemas import (
    EmployeeNotFoundException,
    EmployeeAlreadyActivatedException,
    EmployeeSchema,
)


class EmployeeDAL:

    @staticmethod
    async def create(fio: str, job_title: str = None) -> int:
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

            return employee_id

    @staticmethod
    async def update(
        id: int,
        chat_id: int = None,
        fio: str = None,
        job_title: str = None,
        is_active: bool = None,
    ):
        async with async_session() as session, session.begin():
            q0 = sa.select(Employee.id).where(Employee.id == id)
            employee_id = (await session.execute(q0)).scalar()

            if not employee_id:
                raise EmployeeNotFoundException
            data = {}

            if chat_id:
                data[Employee.chat_id] = chat_id
            if fio:
                data[Employee.fio] = fio
            if job_title:
                data[Employee.job_title] = job_title
            if is_active is not None:
                data[Employee.is_active] = is_active

            q = sa.update(Employee).where(Employee.id == id).values(data)

            await session.execute(q)

    @staticmethod
    async def delete(id: int):
        async with async_session() as session, session.begin():
            q0 = sa.select(Employee.id).where(Employee.id == id)
            employee_id = (await session.execute(q0)).scalar()

            if not employee_id:
                raise EmployeeNotFoundException

            q1 = sa.delete(Employee).where(Employee.id == id)

            await session.execute(q1)

    @staticmethod
    async def get_by_id(id: int) -> EmployeeSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Employee.__table__).where(Employee.id == id)
            employee = (await session.execute(q)).mappings().first()
            if employee:
                return EmployeeSchema(**employee)

    @staticmethod
    async def get_by_chat_id(chat_id: int) -> EmployeeSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Employee.__table__).where(Employee.chat_id == chat_id)
            employee = (await session.execute(q)).mappings().first()
            if employee:
                return EmployeeSchema(**employee)

    @staticmethod
    async def get_all_by_facility_id(facility_id: int) -> List[EmployeeSchema]:
        async with async_session() as session, session.begin():
            q = sa.select(Employee.__table__).where(
                FacilityEmployeeRelationship.facility_id == facility_id,
                FacilityEmployeeRelationship.employee_id == Employee.id,
            )
            employees = (await session.execute(q)).mappings().all()
            return [EmployeeSchema(**employee) for employee in employees]

    @staticmethod
    async def get_all() -> List[EmployeeSchema]:
        async with async_session() as session, session.begin():
            q = sa.select(Employee.__table__)
            employees = (await session.execute(q)).mappings().all()
            return [EmployeeSchema(**employee) for employee in employees]

    @staticmethod
    async def check_by_chat_id(chat_id: int):
        async with async_session() as session, session.begin():
            q = sa.select(Employee.id).where(Employee.chat_id == chat_id)
            return (await session.execute(q)).scalar()

    @staticmethod
    async def check_by_token(token: UUID):
        async with async_session() as session, session.begin():
            q = sa.select(Employee.id).where(Employee.token == token)
            return (await session.execute(q)).scalar()

    @staticmethod
    async def activate(chat_id: int, token: str):
        async with async_session() as session, session.begin():
            result = await session.execute(
                sa.select(Employee.is_active).where(Employee.token == token)
            )
            is_active = result.scalar()
            if is_active is None:
                raise EmployeeNotFoundException

            if not is_active:
                q = (
                    sa.update(Employee)
                    .where(Employee.token == token)
                    .values(chat_id=chat_id, is_active=True)
                )

                await session.execute(q)
            else:
                raise EmployeeAlreadyActivatedException
