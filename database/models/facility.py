import sqlalchemy as sa

from database.models import Base


class Facility(Base):
    __tablename__ = "facility"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    active = sa.Column(sa.Boolean, default=False)
    address = sa.Column(sa.String, nullable=False)
