"""make cohort column required

Revision ID: d5a7c6f6dd4d
Revises: d743d2fd30ba
Create Date: 2024-08-28 16:29:37.377464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a7c6f6dd4d'
down_revision: Union[str, None] = 'd743d2fd30ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('learner', 'cohort',
               existing_type=sa.VARCHAR(length=25),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('learner', 'cohort',
               existing_type=sa.VARCHAR(length=25),
               nullable=True)
    # ### end Alembic commands ###
