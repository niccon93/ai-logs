"""Anchor revision for existing users table (no-op).

Revision ID: 0001_init_users
Revises: 
Create Date: 2025-09-15 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ничего не создаём: таблица users уже существует
    pass


def downgrade() -> None:
    # Откатывать нечего
    pass
