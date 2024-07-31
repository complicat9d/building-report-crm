import sqlalchemy as sa

from database.models import Base


class Employee(Base):
    __tablename__ = "employee"

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(sa.BigInteger, nullable=True, unique=True)
    fio = sa.Column(sa.String, nullable=False)
    job_title = sa.Column(sa.String, nullable=True)
    token = sa.Column(sa.UUID, nullable=False, unique=True)
    is_active = sa.Column(sa.Boolean, default=False)
