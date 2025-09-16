import os
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db import SessionLocal
from app.models.user import User, RoleEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_admin_creds():
    username = os.getenv("ADMIN_USER", "admin")
    password = os.getenv("ADMIN_PASS", "admin123")
    email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    return username, password, email

def ensure_admin(db: Session):
    try:
        any_user = db.execute(select(User).limit(1)).first()
    except (ProgrammingError, OperationalError) as e:
        print(f">>> users table not ready yet: {e}")
        return False

    if any_user:
        print(">>> users table exists and already has rows; skip admin creation")
        return True

    username, password, email = get_admin_creds()
    hashed = pwd_context.hash(password)
    admin = User(username=username, password_hash=hashed, email=email, role=RoleEnum.admin)
    db.add(admin)
    db.commit()
    print(f">>> admin user created: {username}")
    return True

def main():
    db = SessionLocal()
    try:
        ensure_admin(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
