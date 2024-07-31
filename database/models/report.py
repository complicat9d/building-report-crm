import sqlalchemy as sa

from database.models import Base
from database.models.employee import Employee
from database.models.facility import Facility


class Report(Base):
    __tablename__ = "report"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    shift_start = sa.Column(sa.DateTime(timezone=True), nullable=False)
    shift_end = sa.Column(sa.DateTime(timezone=True), nullable=True)
    employee_id = sa.Column(
        sa.ForeignKey(Employee.id, ondelete="CASCADE"), nullable=False
    )
    facility_id = sa.Column(
        sa.ForeignKey(Facility.id, ondelete="CASCADE"), nullable=False
    )
