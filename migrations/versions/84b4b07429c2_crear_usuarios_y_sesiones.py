"""Create the Python authentication tables when they do not exist.

Revision ID: 84b4b07429c2
Revises:
Create Date: 2026-11-19 21:15:58.884579
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "84b4b07429c2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the account and session tables without replacing existing tables."""
    existing_tables = set(sa.inspect(op.get_bind()).get_table_names())

    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("first_name", sa.String(length=100), nullable=False),
            sa.Column("last_name", sa.String(length=100), nullable=False),
            sa.Column("email", sa.String(length=254), nullable=False),
            sa.Column("phone", sa.String(length=30), nullable=True),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column(
                "role",
                sa.Enum(
                    "SUPER_ADMIN",
                    "ADMIN",
                    "MESERO",
                    "COCINERO",
                    "CAJERO",
                    "CLIENTE",
                    name="user_role",
                    native_enum=False,
                    create_constraint=True,
                    length=20,
                ),
                nullable=False,
            ),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            sa.Column(
                "super_admin_slot",
                sa.Integer(),
                sa.Computed(
                    "CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END",
                    persisted=True,
                ),
                nullable=True,
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint(
                "super_admin_slot",
                name="uq_users_single_super_admin",
            ),
        )
        op.create_index(
            "ix_users_role_active",
            "users",
            ["role", "is_active"],
            unique=False,
        )

    # A database may already have an older `user_sessions` table.
    # Leave it in place; the next revision adopts its rows into the current schema.
    if "user_sessions" not in existing_tables:
        op.create_table(
            "user_sessions",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("jti", sa.String(length=255), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            sa.Column("last_activity_at", sa.DateTime(), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=False),
            sa.Column("revoked_at", sa.DateTime(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("ip_address", sa.String(length=45), nullable=True),
            sa.Column("user_agent", sa.String(length=512), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("jti"),
        )
        op.create_index(
            "ix_user_sessions_expires_at",
            "user_sessions",
            ["expires_at"],
            unique=False,
        )
        op.create_index(
            "ix_user_sessions_user_active",
            "user_sessions",
            ["user_id", "is_active"],
            unique=False,
        )


def downgrade() -> None:
    """Remove only tables owned by this revision; preserve pre-existing tables."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "usuario" in tables or "user_sessions_legacy" in tables:
        raise RuntimeError(
            "Downgrade is blocked for a database with adopted account data; "
            "preserve its account and session data and plan a manual rollback."
        )

    if "user_sessions" in tables:
        columns = {column["name"] for column in inspector.get_columns("user_sessions")}
        if "user_id" not in columns:
            raise RuntimeError("Refusing to drop a non-Python user_sessions table.")
        op.drop_index("ix_user_sessions_user_active", table_name="user_sessions")
        op.drop_index("ix_user_sessions_expires_at", table_name="user_sessions")
        op.drop_table("user_sessions")

    if "users" in tables:
        op.drop_index("ix_users_role_active", table_name="users")
        op.drop_table("users")
