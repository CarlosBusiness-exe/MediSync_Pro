"""implement user role field

Revision ID: 43c101bfd223
Revises: c67d44c3ce69
Create Date: 2026-03-19 14:26:00.741977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '43c101bfd223'
down_revision: Union[str, Sequence[str], None] = 'c67d44c3ce69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Manually create the ENUM type first
    op.execute("CREATE TYPE userrole AS ENUM ('ADMIN', 'DOCTOR', 'PATIENT')")
    
    # 2. Now add the column using that type
    op.add_column('users', sa.Column('role', sa.Enum('ADMIN', 'DOCTOR', 'PATIENT', name='userrole'), nullable=True))

def downgrade() -> None:
    # 1. Remove the column
    op.drop_column('users', 'role')
    
    # 2. Manually drop the ENUM type
    op.execute("DROP TYPE userrole")