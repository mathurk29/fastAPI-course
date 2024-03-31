"""add user table

Revision ID: 0add1905a4b6
Revises: 2f6b6b74c82b
Create Date: 2024-03-31 18:33:00.595069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0add1905a4b6'
down_revision: Union[str, None] = '2f6b6b74c82b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
