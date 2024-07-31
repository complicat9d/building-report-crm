import sqlalchemy as sa
from datetime import timedelta, datetime, timezone

from database.models import Token
from schemas import TokenNotFoundException, TokenSchema
from database.session import async_session


class TokenDAL:

    @staticmethod
    async def create(ip_address: str) -> int:
        async with async_session() as session, session.begin():
            q = (
                sa.insert(Token)
                .values(
                    ip_address=ip_address,
                    expires=datetime.now(timezone.utc).replace(tzinfo=None)
                    + timedelta(hours=3, minutes=10),
                )
                .returning(Token.id)
            )

            token_id = (await session.execute(q)).scalar()
            return token_id

    @staticmethod
    async def update(
        ip_address: str, time_increment: timedelta = None, is_expired: bool = None
    ):
        async with async_session() as session, session.begin():
            q = sa.select(Token.id).where(
                sa.and_(Token.ip_address == ip_address, Token.is_expired == False)
            )
            token_id: int = (await session.execute(q)).scalar()

            if not token_id:
                raise TokenNotFoundException

            data = {}

            if time_increment:
                data[Token.expires] = Token.expires + time_increment
            if is_expired is not None:
                data[Token.is_expired] = is_expired

            if data:
                q = sa.update(Token).where(Token.id == token_id).values(data)
                await session.execute(q)

    @staticmethod
    async def get_active(ip_address: str) -> TokenSchema:
        async with async_session() as session, session.begin():
            q = sa.select(Token.id).where(
                sa.and_(Token.ip_address == ip_address, Token.is_expired == False)
            )
            result = (await session.execute(q)).mappings().first()
            if result:
                return TokenSchema(**result)
