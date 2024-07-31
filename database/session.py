from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.db.DATABASE_USER}:"
    f"{settings.db.DATABASE_PASSWORD}@"
    f"{settings.db.DATABASE_HOST}:"
    f"{settings.db.DATABASE_PORT}/"
    f"{settings.db.DATABASE_DB}"
)


def create_engine():
    global engine
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.DEBUG_ENGINE,
        max_overflow=30,
    )
    return engine


async_session = async_sessionmaker(bind=create_engine(), expire_on_commit=True)
