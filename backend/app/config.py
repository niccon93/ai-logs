import os
from functools import lru_cache

@lru_cache
def settings():
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///./local.db"),
        "FERNET_KEYS": os.getenv("FERNET_KEYS",""),
        "JWT_SECRET": os.getenv("JWT_SECRET","changeme"),
        "CORS_ORIGINS": [o.strip() for o in os.getenv("CORS_ORIGINS","").split(",") if o.strip()],
        "REDIS_URL": os.getenv("REDIS_URL","redis://localhost:6379/0"),
        "FRONTEND_URL": os.getenv("FRONTEND_URL","http://localhost:8080"),
        "RATE_LIMIT_DEFAULT": os.getenv("RATE_LIMIT_DEFAULT","60/minute"),
    }
