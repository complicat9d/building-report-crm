"""empty message

Revision ID: 0b6a9bac4d19
Revises: 6cdcd372b28f
Create Date: 2024-07-25 20:18:17.770619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b6a9bac4d19'
down_revision: Union[str, None] = '6cdcd372b28f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.Column('is_expired', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token')
    # ### end Alembic commands ###
