# Backwards compatibility shim so older imports "from app.database import SessionLocal, engine, Base" keep working.
from .db import SessionLocal, engine, Base  # noqa: F401
# --- Compatibility shim: get_db for legacy imports ---
try:
    from .db import SessionLocal as _SessionLocal  # type: ignore
except Exception:
    _SessionLocal = None
try:
    SessionLocal  # type: ignore[name-defined]
except NameError:
    SessionLocal = _SessionLocal  # type: ignore[assignment]

def get_db():
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not configured")
    db = SessionLocal()  # type: ignore[operator]
    try:
        yield db
    finally:
        db.close()
# --- Compatibility shim: get_db for legacy imports ---
try:
    from .db import SessionLocal as _SessionLocal  # type: ignore
except Exception:
    _SessionLocal = None
try:
    SessionLocal  # type: ignore[name-defined]
except NameError:
    SessionLocal = _SessionLocal  # type: ignore[assignment]

def get_db():
    if SessionLocal is None:
        raise RuntimeError("SessionLocal is not configured")
    db = SessionLocal()  # type: ignore[operator]
    try:
        yield db
    finally:
        db.close()
