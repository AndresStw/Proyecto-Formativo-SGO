
"""agregar fecha creacion a reservas

Revision ID: 22d405242756
Revises: c7d9e1f3a5b6
Create Date: 2026-11-26 09:37:06.571634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22d405242756'
down_revision: Union[str, Sequence[str], None] = 'c7d9e1f3a5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'reservas',
        sa.Column(
            'fecha_creacion',
            sa.DateTime(),
            nullable=False
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('reservas', 'fecha_creacion')
