from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import LoginIn, Token, UserOut
from ..models import User
from ..security import verify_password, create_access_token
from ..deps import get_db, get_current_user
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    secret = settings()["JWT_SECRET"] or (settings()["FERNET_KEYS"].split(";")[0] if settings()["FERNET_KEYS"] else "changeme")
    token = create_access_token(sub=str(user.id), role=user.role.value, secret=secret)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
