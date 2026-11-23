"""Adopt Laravel EP-01 accounts into the existing Python auth schema.

Revision ID: c9a7d2e84110
Revises: 84b4b07429c2
Create Date: 2026-11-23
"""

from datetime import datetime, timedelta, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c9a7d2e84110"
down_revision: Union[str, Sequence[str], None] = "84b4b07429c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ROLE_MAP = {
    "cliente": "CLIENTE",
    "mesero": "MESERO",
    "admin": "ADMIN",
    "super_admin": "SUPER_ADMIN",
    "cocinero": "COCINERO",
    "cajero": "CAJERO",
}
ROLE_VALUES = tuple(ROLE_MAP.values())
ROLE_CHECK = "role IN (" + ", ".join(f"'{role}'" for role in ROLE_VALUES) + ")"
MAX_SIGNED_INT = 2_147_483_647


def _bind():
    return op.get_bind()


def _inspector():
    return sa.inspect(_bind())


def _tables() -> set[str]:
    return set(_inspector().get_table_names())


def _columns(table_name: str) -> set[str]:
    return {column["name"] for column in _inspector().get_columns(table_name)}


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _to_datetime(value, fallback: datetime) -> datetime:
    if value is None:
        return fallback
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is not None:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    raise RuntimeError("A legacy account/session has an unsupported date value.")


def _normalize_email(value) -> str:
    return str(value or "").strip().lower()


def _normalize_phone(value) -> str | None:
    phone = str(value).strip() if value is not None else ""
    return phone or None


def _map_role(value, user_id: int) -> str:
    role = str(value or "").strip().lower().replace("-", "_").replace(" ", "_")
    if role not in ROLE_MAP:
        raise RuntimeError(
            f"Cannot migrate usuario.idUsuario={user_id}: unsupported role. "
            "No schema or account data was changed."
        )
    return ROLE_MAP[role]


def _map_active(value, deleted_at) -> bool:
    if deleted_at is not None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    normalized = str(value or "").strip().lower()
    if normalized in {"1", "true", "activo", "active", "enabled", "habilitado", "si", "sí"}:
        return True
    if normalized in {"0", "false", "inactivo", "inactive", "disabled", "deshabilitado", "no"}:
        return False
    raise RuntimeError(
        "Cannot migrate a usuario row with an unrecognized estado value. "
        "No schema or account data was changed."
    )


def _read_user_rows(table_name: str, id_column: str) -> list[dict]:
    if table_name not in _tables():
        return []
    expected = {
        "idUsuario", "primerNombre", "segundoNombre", "primerApellido",
        "segundoApellido", "telefono", "email", "direccion", "password_hash",
        "rol", "estado", "created_at", "updated_at", "deleted_at",
    }
    available = _columns(table_name)
    required = {"idUsuario", "primerNombre", "primerApellido", "email", "password_hash", "rol"}
    if not required.issubset(available):
        raise RuntimeError(
            f"The legacy `{table_name}` table is missing required EP-01 columns: "
            f"{', '.join(sorted(required - available))}. No schema or account data was changed."
        )

    selected = [column for column in expected if column in available]
    statement = sa.text(
        f"SELECT {', '.join(f'`{column}`' for column in selected)} "
        f"FROM `{table_name}` ORDER BY `{id_column}`"
    )
    return [dict(row) for row in _bind().execute(statement).mappings()]


def _source_accounts() -> list[dict]:
    if "usuario" not in _tables():
        return []

    accounts = []
    for row in _read_user_rows("usuario", "idUsuario"):
        user_id = int(row["idUsuario"])
        if user_id <= 0 or user_id > MAX_SIGNED_INT:
            raise RuntimeError(
                f"Cannot migrate usuario.idUsuario={user_id}: it does not fit in the "
                "existing Python users.id column. No schema or account data was changed."
            )

        first_name = str(row.get("primerNombre") or "").strip()
        last_name = str(row.get("primerApellido") or "").strip()
        email = _normalize_email(row.get("email"))
        password_hash = str(row.get("password_hash") or "")
        if not first_name or not last_name or not email or not password_hash:
            raise RuntimeError(
                f"Cannot migrate usuario.idUsuario={user_id}: a required account field is empty. "
                "No schema or account data was changed."
            )

        account = {
            "id": user_id,
            "first_name": first_name,
            "second_name": str(row["segundoNombre"]).strip() if row.get("segundoNombre") else None,
            "last_name": last_name,
            "second_last_name": str(row["segundoApellido"]).strip() if row.get("segundoApellido") else None,
            "email": email,
            "phone": _normalize_phone(row.get("telefono")),
            "address": str(row["direccion"]).strip() if row.get("direccion") else None,
            "password_hash": password_hash,
            "role": _map_role(row.get("rol"), user_id),
            "is_active": _map_active(row.get("estado", 1), row.get("deleted_at")),
            "created_at": _to_datetime(row.get("created_at"), _utc_now_naive()),
            "updated_at": _to_datetime(row.get("updated_at"), _utc_now_naive()),
        }

        limits = {
            "first_name": 100,
            "second_name": 45,
            "last_name": 100,
            "second_last_name": 45,
            "email": 254,
            "phone": 30,
            "address": 255,
            "password_hash": 255,
        }
        for field, limit in limits.items():
            if account[field] is not None and len(account[field]) > limit:
                raise RuntimeError(
                    f"Cannot migrate usuario.idUsuario={user_id}: `{field}` exceeds "
                    f"the Python users column limit ({limit}). No schema or account data was changed."
                )
        accounts.append(account)
    return accounts


def _existing_accounts() -> list[dict]:
    if "users" not in _tables():
        return []
    required = {"id", "first_name", "last_name", "email", "password_hash", "role"}
    available = _columns("users")
    if not required.issubset(available):
        raise RuntimeError(
            "The existing `users` table does not match the Python account schema. "
            f"Missing: {', '.join(sorted(required - available))}. "
            "No schema or account data was changed."
        )
    table = sa.Table("users", sa.MetaData(), autoload_with=_bind())
    return [dict(row) for row in _bind().execute(sa.select(table)).mappings()]


def _check_account_conflicts(source: list[dict], existing: list[dict]) -> None:
    source_emails: set[str] = set()
    source_phones: set[str] = set()
    existing_by_id = {int(row["id"]): row for row in existing}
    existing_emails = {_normalize_email(row.get("email")): int(row["id"]) for row in existing}
    existing_phones = {
        _normalize_phone(row.get("phone")): int(row["id"])
        for row in existing
        if _normalize_phone(row.get("phone"))
    }

    for account in source:
        user_id = account["id"]
        if account["email"] in source_emails:
            raise RuntimeError("Duplicate email values exist in `usuario`; migration stopped before changes.")
        source_emails.add(account["email"])
        phone = account["phone"]
        if phone and phone in source_phones:
            raise RuntimeError("Duplicate phone values exist in `usuario`; migration stopped before changes.")
        if phone:
            source_phones.add(phone)

        existing_id_for_email = existing_emails.get(account["email"])
        if existing_id_for_email is not None and existing_id_for_email != user_id:
            raise RuntimeError(
                "An imported email already belongs to a different `users` row; "
                "migration stopped before changes."
            )
        existing_id_for_phone = existing_phones.get(phone) if phone else None
        if existing_id_for_phone is not None and existing_id_for_phone != user_id:
            raise RuntimeError(
                "An imported phone already belongs to a different `users` row; "
                "migration stopped before changes."
            )

        current = existing_by_id.get(user_id)
        if current is not None:
            core_fields = ("first_name", "last_name", "email", "password_hash", "role")
            if any(
                str(current.get(field) or "").strip().lower()
                != str(account[field] or "").strip().lower()
                for field in core_fields
            ):
                raise RuntimeError(
                    f"`users.id={user_id}` conflicts with `usuario.idUsuario={user_id}`; "
                    "migration stopped before changes."
                )

    super_admins = sum(row["role"] == "SUPER_ADMIN" for row in source)
    super_admins += sum(str(row.get("role")) == "SUPER_ADMIN" for row in existing)
    for account in source:
        current = existing_by_id.get(account["id"])
        if current is not None and str(current.get("role")) == "SUPER_ADMIN":
            super_admins -= 1
    if super_admins > 1:
        raise RuntimeError(
            "The merged accounts would contain more than one SUPER_ADMIN, "
            "which conflicts with the existing Python users constraint."
        )


def _read_legacy_sessions() -> list[dict]:
    tables = _tables()
    legacy_table = None
    if "user_sessions" in tables:
        columns = _columns("user_sessions")
        if "idUsuario" in columns and "user_id" not in columns:
            legacy_table = "user_sessions"
    if "user_sessions_legacy" in tables:
        if legacy_table is not None:
            raise RuntimeError(
                "Both legacy session table names exist; inspect them before migrating to avoid duplication."
            )
        legacy_table = "user_sessions_legacy"
    if legacy_table is None:
        return []

    columns = _columns(legacy_table)
    required = {"id", "idUsuario", "jti", "last_activity_at", "expires_at"}
    if not required.issubset(columns):
        raise RuntimeError(
            f"The legacy session table is missing: {', '.join(sorted(required - columns))}. "
            "Migration stopped before changes."
        )
    table = sa.Table(legacy_table, sa.MetaData(), autoload_with=_bind())
    return [dict(row) for row in _bind().execute(sa.select(table)).mappings()]


def _preflight() -> tuple[list[dict], list[dict]]:
    if "users" not in _tables():
        raise RuntimeError("The base `users` migration has not run; no changes were made.")

    source = _source_accounts()
    existing = _existing_accounts()
    _check_account_conflicts(source, existing)

    sessions = _read_legacy_sessions()
    valid_user_ids = {int(row["id"]) for row in existing}
    valid_user_ids.update(account["id"] for account in source)
    for session in sessions:
        user_id = int(session["idUsuario"])
        if user_id not in valid_user_ids:
            raise RuntimeError(
                "A legacy session references an account that will not exist in `users`; "
                "migration stopped before changes."
            )
        if int(session["id"]) <= 0 or int(session["id"]) > MAX_SIGNED_INT:
            raise RuntimeError("A legacy session ID exceeds the Python schema limit; migration stopped.")
    return source, sessions


def _has_unique(table: str, column: str) -> bool:
    inspector = _inspector()
    if any(column in item.get("column_names", []) for item in inspector.get_unique_constraints(table)):
        return True
    return any(
        item.get("unique") and column in item.get("column_names", [])
        for item in inspector.get_indexes(table)
    )


def _ensure_user_columns() -> None:
    available = _columns("users")
    optional_columns = (
        ("second_name", sa.String(length=45)),
        ("second_last_name", sa.String(length=45)),
        ("address", sa.String(length=255)),
    )
    for name, column_type in optional_columns:
        if name not in available:
            op.add_column("users", sa.Column(name, column_type, nullable=True))

    available = _columns("users")
    if "super_admin_slot" not in available:
        op.add_column(
            "users",
            sa.Column(
                "super_admin_slot",
                sa.Integer(),
                sa.Computed("CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END", persisted=True),
                nullable=True,
            ),
        )


def _ensure_role_check() -> None:
    constraints = _inspector().get_check_constraints("users")
    role_constraints = [
        item for item in constraints
        if "role" in str(item.get("sqltext", "")).lower()
    ]
    desired_values = set(ROLE_VALUES)
    current_values = set()
    for item in role_constraints:
        sqltext = str(item.get("sqltext", ""))
        current_values.update(role for role in ROLE_VALUES if f"'{role}'" in sqltext)
    if desired_values.issubset(current_values):
        return

    if _bind().dialect.name == "mysql":
        preparer = _bind().dialect.identifier_preparer
        for item in role_constraints:
            name = item.get("name")
            if not name:
                raise RuntimeError(
                    "An unnamed role check constraint cannot be safely replaced automatically."
                )
            op.execute(sa.text(f"ALTER TABLE users DROP CHECK {preparer.quote(name)}"))
        op.execute(sa.text(f"ALTER TABLE users ADD CONSTRAINT user_role CHECK ({ROLE_CHECK})"))
        return

    with op.batch_alter_table("users") as batch:
        for item in role_constraints:
            name = item.get("name")
            if not name:
                raise RuntimeError(
                    "An unnamed role check constraint cannot be safely replaced automatically."
                )
            batch.drop_constraint(name, type_="check")
        batch.create_check_constraint("user_role", ROLE_CHECK)


def _ensure_user_constraints() -> None:
    if not _has_unique("users", "email"):
        op.create_index("uq_users_email", "users", ["email"], unique=True)
    if not _has_unique("users", "phone"):
        op.create_index("uq_users_phone", "users", ["phone"], unique=True)
    if not _has_unique("users", "super_admin_slot"):
        with op.batch_alter_table("users") as batch:
            batch.create_unique_constraint(
                "uq_users_single_super_admin", ["super_admin_slot"]
            )

    indexes = {item["name"] for item in _inspector().get_indexes("users")}
    if "ix_users_role_active" not in indexes and {"role", "is_active"}.issubset(_columns("users")):
        op.create_index("ix_users_role_active", "users", ["role", "is_active"])


def _ensure_password_reset_table() -> None:
    tables = _tables()
    if "password_reset_tokens" not in tables:
        op.create_table(
            "password_reset_tokens",
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("token", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("email"),
        )
        return

    required = {"email", "token", "created_at"}
    available = _columns("password_reset_tokens")
    if not required.issubset(available):
        raise RuntimeError(
            "The existing `password_reset_tokens` table is not Laravel-compatible; "
            "it was left untouched."
        )


def _create_user_sessions() -> None:
    if "user_sessions" in _tables():
        return
    op.create_table(
        "user_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("jti", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
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
    op.create_index("ix_user_sessions_expires_at", "user_sessions", ["expires_at"])
    op.create_index("ix_user_sessions_user_active", "user_sessions", ["user_id", "is_active"])


def _ensure_sessions(source_sessions: list[dict]) -> None:
    tables = _tables()
    if "user_sessions" in tables and "idUsuario" in _columns("user_sessions"):
        if "user_sessions_legacy" in tables:
            raise RuntimeError("Cannot rename legacy sessions because the archive table already exists.")
        op.rename_table("user_sessions", "user_sessions_legacy")

    _create_user_sessions()
    session_columns = _columns("user_sessions")
    required = {
        "id", "user_id", "jti", "created_at", "last_activity_at", "expires_at",
        "revoked_at", "is_active", "ip_address", "user_agent",
    }
    if not required.issubset(session_columns):
        if "revoked_at" in required - session_columns and {"id", "user_id", "jti"}.issubset(session_columns):
            op.add_column("user_sessions", sa.Column("revoked_at", sa.DateTime(), nullable=True))
            session_columns.add("revoked_at")
        if not required.issubset(session_columns):
            raise RuntimeError(
                "The existing Python `user_sessions` table has an unsupported schema; "
                "legacy session data was preserved."
            )

    if not source_sessions:
        return

    table = sa.Table("user_sessions", sa.MetaData(), autoload_with=_bind())
    current_ids = {
        int(row[0]) for row in _bind().execute(sa.select(table.c.id)).all()
    }
    now = _utc_now_naive()
    rows_to_insert = []
    for legacy in source_sessions:
        session_id = int(legacy["id"])
        if session_id in current_ids:
            continue
        created_at = _to_datetime(legacy.get("created_at"), now)
        last_activity_at = _to_datetime(legacy.get("last_activity_at"), created_at)
        expires_at = _to_datetime(legacy.get("expires_at"), created_at + timedelta(seconds=1))
        rows_to_insert.append(
            {
                "id": session_id,
                "user_id": int(legacy["idUsuario"]),
                # These Laravel/Sanctum identifiers are not valid Python JWTs.
                # Prefix them and mark them revoked so they can never authenticate.
                "jti": f"legacy-{session_id}-{str(legacy.get('jti') or '')}"[:255],
                "created_at": created_at,
                "last_activity_at": last_activity_at,
                "expires_at": expires_at,
                "revoked_at": now,
                "is_active": False,
                "ip_address": legacy.get("ip_address"),
                "user_agent": str(legacy["user_agent"])[:512] if legacy.get("user_agent") else None,
            }
        )
    if rows_to_insert:
        _bind().execute(table.insert(), rows_to_insert)


def upgrade() -> None:
    """Preflight, then merge legacy Laravel accounts into `users` safely."""
    source_accounts, source_sessions = _preflight()

    _ensure_user_columns()
    _ensure_role_check()
    _ensure_user_constraints()
    _ensure_password_reset_table()

    if source_accounts:
        users = sa.Table("users", sa.MetaData(), autoload_with=_bind())
        existing_rows = {
            int(row["id"]): dict(row)
            for row in _bind().execute(sa.select(users)).mappings()
        }
        new_rows = []
        supplemental_updates = []
        for account in source_accounts:
            current = existing_rows.get(account["id"])
            if current is None:
                new_rows.append(account)
                continue
            update = {"id": account["id"]}
            for field in ("second_name", "second_last_name", "address", "phone"):
                if field in users.c and not current.get(field) and account.get(field):
                    update[field] = account[field]
            if len(update) > 1:
                supplemental_updates.append(update)
        if new_rows:
            _bind().execute(users.insert(), new_rows)
        for update in supplemental_updates:
            user_id = update.pop("id")
            _bind().execute(users.update().where(users.c.id == user_id).values(**update))

    _ensure_sessions(source_sessions)


def downgrade() -> None:
    """Require a manual backup-based rollback to protect adopted Laravel data."""
    raise RuntimeError(
        "This account adoption is intentionally irreversible through Alembic. "
        "Restore a verified database backup to roll back; Laravel tables and records were preserved."
    )
