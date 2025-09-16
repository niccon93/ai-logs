
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_role
from ..models.user import User
router = APIRouter(tags=["admin"])
@router.get("/users", dependencies=[Depends(require_role("admin"))])
def list_users(db: Session = Depends(get_db)):
    rows = db.query(User).order_by(User.id).all()
    def row(u: User): return {"id": u.id, "username": u.username, "role": (getattr(u.role,'value', u.role)), "email": u.email}
    return [row(u) for u in rows]
