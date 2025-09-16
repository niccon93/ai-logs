from logging.config import fileConfig
import os, sys
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Чтобы импорты "app.*" работали при запуске Alembic внутри контейнера
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Подтянуть Base и модели, чтобы metadata была полной
def import_models():
    import importlib
    modules = [
        "app.models",
        "app.models.user",
        "app.models.users",
        "app.models.auth",
    ]
    for m in modules:
        try:
            importlib.import_module(m)
        except Exception:
            pass

from app.database import Base  # noqa: E402
import_models()

target_metadata = Base.metadata

def get_url():
    # Предпочитаем переменную окружения DATABASE_URL (Docker),
    # иначе берём sqlalchemy.url из alembic.ini
    return os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
