"""Ensure users.created_at is always set (default + trigger).

Revision ID: 0002_users_created_at_guard
Revises: 0001_init_users
Create Date: 2025-09-15 00:01:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_users_created_at_guard"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) DEFAULT now() для users.created_at
    op.alter_column(
        "users",
        "created_at",
        server_default=sa.text("now()"),
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )

    # 2) Триггер: если вставляют NULL, подставить now()
    op.execute(
        """
        CREATE OR REPLACE FUNCTION trg_users_set_created_at()
        RETURNS trigger AS $$
        BEGIN
            IF NEW.created_at IS NULL THEN
                NEW.created_at := now();
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute("DROP TRIGGER IF EXISTS trg_users_created_at ON users;")

    op.execute(
        """
        CREATE TRIGGER trg_users_created_at
        BEFORE INSERT ON users
        FOR EACH ROW
        EXECUTE FUNCTION trg_users_set_created_at();
        """
    )


def downgrade() -> None:
    # Удаляем триггер и функцию
    op.execute("DROP TRIGGER IF EXISTS trg_users_created_at ON users;")
    op.execute("DROP FUNCTION IF EXISTS trg_users_set_created_at;")

    # Сбрасываем default у столбца
    op.alter_column(
        "users",
        "created_at",
        server_default=None,
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
    )
