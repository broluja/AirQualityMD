"""Create Table users

Revision ID: 6e713acc1dde
Revises: 
Create Date: 2022-10-01 21:36:04.460890

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '6e713acc1dde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('email', sa.String(99), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_user_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    op.drop_table('users')
