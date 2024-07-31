import sqlalchemy as sa

from database.models import Base
from database.models.report import Report


class Pause(Base):
    __tablename__ = "pause"

    id = sa.Column(sa.Integer, primary_key=True)
    start = sa.Column(sa.DateTime(timezone=True), nullable=False)
    end = sa.Column(sa.DateTime(timezone=True), nullable=True)
    report_id = sa.Column(sa.ForeignKey(Report.id, ondelete="CASCADE"), nullable=False)
