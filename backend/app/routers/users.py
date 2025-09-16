from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas import UserOut, UserCreate
from ..models import User, RoleEnum
from ..deps import get_db, require_admin
from ..security import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(User).order_by(User.id).all()

@router.post("/", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username already exists")
    user = User(username=data.username, email=data.email, role=RoleEnum(data.role), hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return user
