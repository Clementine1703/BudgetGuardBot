"""add expenses and expense_category tables

Revision ID: 0002
Revises: 0001
Create Date: 2025-05-06 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'expense_category',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), unique=True, nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('tg_user.id'), nullable=False),
    )

    op.create_table(
        'expense',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('expense_category.id'), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('comment', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)),
    )


def downgrade() -> None:
    op.drop_table('expense')
    op.drop_table('expense_category')
