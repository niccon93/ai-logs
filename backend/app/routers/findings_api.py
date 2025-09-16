
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Literal
from ..db import get_db
from ..models.finding import Finding
from sqlalchemy import desc, asc
router = APIRouter(prefix="/findings", tags=["findings"])
@router.get("")
def list_findings(db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=500),
    severity: Optional[str] = None, search: Optional[str] = None, sort: Optional[str] = "ts", order: Literal["asc","desc"] = "desc"):
    q = db.query(Finding); 
    if severity: q = q.filter(Finding.severity == severity)
    if search: q = q.filter(Finding.message.ilike(f"%{search}%"))
    sort_col = getattr(Finding, sort, None)
    if sort_col is None: raise HTTPException(400, "Invalid sort column")
    q = q.order_by(asc(sort_col) if order=="asc" else desc(sort_col))
    total = q.count(); items = q.offset((page-1)*size).limit(size).all()
    to_d = lambda o: {"id": o.id, "dataset_id": o.dataset_id, "model_id": o.model_id, "severity": o.severity,
                      "ts": o.ts.isoformat() if o.ts else None, "host": o.host, "app": o.app, "template_id": o.template_id, "message": o.message}
    return {"page": page, "size": size, "total": total, "items": [to_d(i) for i in items]}
