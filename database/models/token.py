import sqlalchemy as sa

from database.models import Base


class Token(Base):
    __tablename__ = "token"

    id = sa.Column(sa.Integer, primary_key=True)
    ip_address = sa.Column(sa.String, nullable=False)
    expires = sa.Column(sa.DateTime, nullable=False)
    is_expired = sa.Column(sa.Boolean, default=False)
