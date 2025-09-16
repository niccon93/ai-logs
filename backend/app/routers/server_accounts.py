from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db
from ..models.server_account import ServerAccount  # фикс импорта
from ..schemas.server_accounts import ServerAccountCreate, ServerAccountRead

router = APIRouter(prefix="/server-accounts", tags=["server-accounts"])


@router.post("/", response_model=ServerAccountRead, status_code=status.HTTP_201_CREATED)
def create_server_account(payload: ServerAccountCreate, db: Session = Depends(get_db)):
    account = ServerAccount(**payload.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=ServerAccountRead)
def get_server_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(ServerAccount).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="ServerAccount not found")
    return account
