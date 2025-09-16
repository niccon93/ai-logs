from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import require_admin, get_db
from ..models import ServerAccount, Source

router = APIRouter(prefix="/examples", tags=["examples"])

@router.post("/import")
def import_examples(db: Session = Depends(get_db), _=Depends(require_admin)):
    # seed minimal demo
    if not db.query(ServerAccount).first():
        acc = ServerAccount(name="demo", username="root", public_key="ssh-rsa AAA... demo", description="Demo account")
        db.add(acc); db.commit(); db.refresh(acc)
        src = Source(server_account_id=acc.id, path_glob="/var/log/*.log", interval_minutes=5, enabled=True)
        db.add(src); db.commit()
    return {"status":"ok"}
