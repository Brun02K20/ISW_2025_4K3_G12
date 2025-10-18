"""change_talle_to_string

Revision ID: 84419b33df77
Revises: 167efe3dfe2f
Create Date: 2025-10-18 16:00:32.381208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84419b33df77'
down_revision: Union[str, None] = '167efe3dfe2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cambiar el tipo de dato del campo talle de Integer a String
    op.alter_column('visitante', 'talle',
                    type_=sa.String(),
                    existing_type=sa.Integer(),
                    nullable=True)  # Mantener nullable ya que puede ser None


def downgrade() -> None:
    # Revertir el cambio: de String a Integer
    op.alter_column('visitante', 'talle',
                    type_=sa.Integer(),
                    existing_type=sa.String(),
                    nullable=True)
