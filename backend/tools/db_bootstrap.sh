#!/usr/bin/env bash
set -euo pipefail

cd /app/backend 2>/dev/null || cd "$(dirname "$0")/.."

: "${DATABASE_URL:=postgresql+psycopg://ailog:ailog@db:5432/ailog}"
: "${ADMIN_USER:=admin}"
: "${ADMIN_PASS:=admin123}"
: "${ADMIN_EMAIL:=admin@example.com}"

echo ">>> Waiting for Postgres"
python -m scripts.wait_for_postgres

echo ">>> Ensure Alembic template exists"
mkdir -p alembic/versions
if [ ! -f "alembic/script.py.mako" ]; then
  cat > alembic/script.py.mako <<'MAKO'
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade():
% if upgrades:
    ${upgrades | indent(4)}
% else:
    pass
% endif

def downgrade():
% if downgrades:
    ${downgrades | indent(4)}
% else:
    pass
% endif
MAKO
fi

echo ">>> Generate initial revision if none exists"
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions)" ]; then
  alembic revision --autogenerate -m "init schema"
else
  echo "    (versions already present, skipping revision autogenerate)"
fi

echo ">>> Apply migrations"
alembic upgrade head

echo ">>> Init admin"
ADMIN_USER="$ADMIN_USER" ADMIN_PASS="$ADMIN_PASS" ADMIN_EMAIL="$ADMIN_EMAIL" \
  python -m scripts.init_admin

echo ">>> Bootstrap done"
