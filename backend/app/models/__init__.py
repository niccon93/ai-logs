"""
Пакет моделей. Экспортируем основные сущности.
Если модуля 'server_account' нет, не падаем при импорте.
"""
from .user import User, RoleEnum  # основной источник истины

# Мягкая поддержка ServerAccount: если модуля нет — не валимся на импорте
try:
    from .server_account import ServerAccount  # type: ignore  # noqa: F401
except Exception:
    ServerAccount = None  # type: ignore

__all__ = ["User", "RoleEnum", "ServerAccount"]
