"""add content column to post table

Revision ID: 2f6b6b74c82b
Revises: 14274f4ee52e
Create Date: 2024-03-31 18:10:26.818660

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2f6b6b74c82b"
down_revision: Union[str, None] = "14274f4ee52e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
