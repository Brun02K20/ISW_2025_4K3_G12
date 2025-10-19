"""add_descripcion_to_actividad

Revision ID: fb528749b4f4
Revises: 131dd039c8e3
Create Date: 2025-10-19 16:26:28.859613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb528749b4f4'
down_revision: Union[str, None] = '131dd039c8e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar columna descripcion como String nullable
    op.add_column('actividad', sa.Column('descripcion', sa.String(), nullable=True))


def downgrade() -> None:
    # Eliminar columna descripcion
    op.drop_column('actividad', 'descripcion')
