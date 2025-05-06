"""init

Revision ID: 0001
Revises: 
Create Date: 2025-04-13 21:18:46.417337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'tg_user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tg_id', sa.BigInteger(), unique=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tg_user')
