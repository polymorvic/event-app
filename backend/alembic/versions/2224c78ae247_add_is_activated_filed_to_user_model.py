"""add is_activated filed to user model

Revision ID: 2224c78ae247
Revises: e5c30eb54b1c
Create Date: 2025-07-07 16:15:49.330220

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2224c78ae247"
down_revision: Union[str, None] = "e5c30eb54b1c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("is_activated", sa.Boolean(), nullable=True))
    op.execute("""
               UPDATE users set is_activated = false
               """)
    op.alter_column("users", "is_activated", existing_type=sa.Boolean(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_activated")
