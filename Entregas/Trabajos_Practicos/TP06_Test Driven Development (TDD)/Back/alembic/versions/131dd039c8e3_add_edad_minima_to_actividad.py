"""add_edad_minima_to_actividad

Revision ID: 131dd039c8e3
Revises: 84419b33df77
Create Date: 2025-10-19 16:18:26.323319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131dd039c8e3'
down_revision: Union[str, None] = '84419b33df77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar columna edad_minima como Integer nullable
    op.add_column('actividad', sa.Column('edad_minima', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Eliminar columna edad_minima
    op.drop_column('actividad', 'edad_minima')
