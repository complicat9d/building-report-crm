import os
import sqlalchemy as sa
from typing import List

from database.models import File
from database.session import async_session
from schemas import FileSchema, FileNotFoundException, PhotoLimitExceededException
from config import settings


class FileDAL:

    @staticmethod
    async def create(path: str, report_id: int) -> int:
        async with async_session() as session, session.begin():
            q0 = sa.select(sa.func.count(File.id))
            amount = (await session.execute(q0)).scalar()

            if amount == settings.PHOTO_LIMIT:
                raise PhotoLimitExceededException

            q = (
                sa.insert(File)
                .values({File.path: path, File.report_id: report_id})
                .returning(File.id)
            )

            file_id = (await session.execute(q)).scalar()

            return file_id

    @staticmethod
    async def delete(id: int):
        async with async_session() as session, session.begin():
            q0 = sa.select(File.path).where(File.id == id)
            path = (await session.execute(q0)).scalar()

            if not path:
                raise FileNotFoundException

            if os.path.exists(path):
                os.remove(path)

            q = sa.delete(File).where(File.id == id)

            await session.execute(q)

    @staticmethod
    async def get_by_report_id(report_id: int) -> List[FileSchema]:
        async with async_session() as session, session.begin():
            q = sa.select(File.__table__).where(File.report_id == report_id)
            files = (await session.execute(q)).mappings().all()
            return [FileSchema(**file) for file in files]

    @staticmethod
    async def get(id: int) -> FileSchema:
        async with async_session() as session, session.begin():
            q = sa.select(File.__table__).where(File.id == id)
            file = (await session.execute(q)).first().all()
            return FileSchema(**file)
