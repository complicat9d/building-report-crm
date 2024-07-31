import sqlalchemy as sa

from database.models import Base
from database.models.report import Report


class File(Base):
    __tablename__ = "file"

    id = sa.Column(sa.Integer, primary_key=True)
    path = sa.Column(sa.String, nullable=False)
    report_id = sa.Column(sa.ForeignKey(Report.id, ondelete="CASCADE"), nullable=False)
