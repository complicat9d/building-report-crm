import sqlalchemy as sa

from database.models import Base
from database.models.employee import Employee


class Message(Base):
    __tablename__ = "message"

    id = sa.Column(sa.Integer, primary_key=True)
    chat_id = sa.Column(
        sa.ForeignKey(Employee.chat_id, ondelete="CASCADE"), nullable=False
    )
    msg_ids = sa.Column(sa.ARRAY(sa.Integer), default=[])
