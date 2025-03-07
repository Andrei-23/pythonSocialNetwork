"""sth changed

Revision ID: c7c303c9534a
Revises: 5bb433f92582
Create Date: 2025-03-07 21:01:24.996769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7c303c9534a'
down_revision: Union[str, None] = '5bb433f92582'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('majors', sa.Column('count_students', sa.Integer(), server_default=sa.text('0'), nullable=False))
    op.drop_column('majors', 'count_users')
    op.add_column('users', sa.Column('address', sa.Text(), nullable=False))
    op.add_column('users', sa.Column('enrollment_year', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('course', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('special_notes', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'special_notes')
    op.drop_column('users', 'course')
    op.drop_column('users', 'enrollment_year')
    op.drop_column('users', 'address')
    op.add_column('majors', sa.Column('count_users', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.drop_column('majors', 'count_students')
    # ### end Alembic commands ###
