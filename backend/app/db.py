
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://ailog:ailog@db:5432/ailog")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
