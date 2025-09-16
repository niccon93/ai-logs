from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pwd_context.verify(p, hashed)

def create_access_token(sub: str, role: str, secret: str, expires_minutes: int = 120) -> str:
    payload = {"sub": sub, "role": role, "exp": int((datetime.utcnow() + timedelta(minutes=expires_minutes)).timestamp())}
    return jwt.encode(payload, secret, algorithm="HS256")
