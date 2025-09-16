from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..schemas import SourceIn, SourceOut
from ..models import Source
from ..deps import get_db, require_admin

router = APIRouter(prefix="/sources", tags=["sources"])

@router.get("/", response_model=List[SourceOut])
def list_sources(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    return db.query(Source).order_by(Source.id).all()

@router.post("/", response_model=SourceOut)
def create_source(data: SourceIn, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    src = Source(**data.dict())
    db.add(src); db.commit(); db.refresh(src)
    return src
