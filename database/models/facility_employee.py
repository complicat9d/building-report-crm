import sqlalchemy as sa

from database.models import Base
from database.models.employee import Employee
from database.models.facility import Facility


class FacilityEmployeeRelationship(Base):
    __tablename__ = "facility_employee_relationship"

    id = sa.Column(sa.Integer, primary_key=True)
    employee_id = sa.Column(
        sa.ForeignKey(Employee.id, ondelete="CASCADE"), nullable=False
    )
    facility_id = sa.Column(
        sa.ForeignKey(Facility.id, ondelete="CASCADE"), nullable=False
    )
