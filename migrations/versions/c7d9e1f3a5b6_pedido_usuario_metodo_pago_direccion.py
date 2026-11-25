"""pedido usuario, metodo de pago y direccion

Revision ID: c7d9e1f3a5b6
Revises: e09827dd3b4d
Create Date: 2026-11-24 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c7d9e1f3a5b6'
down_revision: Union[str, Sequence[str], None] = 'e09827dd3b4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _nombre_fk(db, columna: str) -> str | None:
    return db.execute(
        sa.text(
            "SELECT CONSTRAINT_NAME "
            "FROM information_schema.KEY_COLUMN_USAGE "
            "WHERE TABLE_SCHEMA = DATABASE() "
            "AND TABLE_NAME = 'pedido' "
            "AND COLUMN_NAME = :columna "
            "AND REFERENCED_TABLE_NAME = 'users'"
        ),
        {"columna": columna},
    ).scalar()


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'pedido',
        sa.Column('direccion_entrega', sa.String(length=255), nullable=True),
    )
    op.add_column(
        'pedido',
        sa.Column('MetodoPago_idMetodoPago', sa.Integer(), nullable=True),
    )
    op.create_index(
        op.f('ix_pedido_MetodoPago_idMetodoPago'),
        'pedido',
        ['MetodoPago_idMetodoPago'],
        unique=False,
    )
    op.create_foreign_key(
        'fk_pedido_metodo_pago',
        'pedido',
        'metodospago',
        ['MetodoPago_idMetodoPago'],
        ['idMetodoPago'],
    )

    fk_usuario = _nombre_fk(op.get_bind(), 'Cliente_id_cliente')

    if fk_usuario:
        op.drop_constraint(fk_usuario, 'pedido', type_='foreignkey')

    op.alter_column(
        'pedido',
        'Cliente_id_cliente',
        new_column_name='users_id_users',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.drop_index(
        op.f('ix_pedido_Cliente_id_cliente'),
        table_name='pedido',
    )
    op.create_index(
        op.f('ix_pedido_users_id_users'),
        'pedido',
        ['users_id_users'],
        unique=False,
    )
    op.create_foreign_key(
        'fk_pedido_usuario',
        'pedido',
        'users',
        ['users_id_users'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    fk_usuario = _nombre_fk(op.get_bind(), 'users_id_users')

    if fk_usuario:
        op.drop_constraint(fk_usuario, 'pedido', type_='foreignkey')

    op.alter_column(
        'pedido',
        'users_id_users',
        new_column_name='Cliente_id_cliente',
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
    op.drop_index(
        op.f('ix_pedido_users_id_users'),
        table_name='pedido',
    )
    op.create_index(
        op.f('ix_pedido_Cliente_id_cliente'),
        'pedido',
        ['Cliente_id_cliente'],
        unique=False,
    )
    op.create_foreign_key(
        'pedido_ibfk_1',
        'pedido',
        'users',
        ['Cliente_id_cliente'],
        ['id'],
    )

    op.drop_constraint(
        'fk_pedido_metodo_pago',
        'pedido',
        type_='foreignkey',
    )
    op.drop_index(
        op.f('ix_pedido_MetodoPago_idMetodoPago'),
        table_name='pedido',
    )
    op.drop_column('pedido', 'MetodoPago_idMetodoPago')
    op.drop_column('pedido', 'direccion_entrega')
