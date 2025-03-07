"""fix foreignkey

Revision ID: 5bfc6bba3a0e
Revises: c275a7b528b1
Create Date: 2025-03-07 20:42:27.299352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bfc6bba3a0e'
down_revision: Union[str, None] = 'c275a7b528b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('major_id', sa.Integer(), server_default=sa.text('1'), nullable=False))
    op.create_foreign_key(None, 'users', 'majors', ['major_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'major_id')
    # ### end Alembic commands ###
