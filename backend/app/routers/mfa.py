
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pyotp
from ..deps import get_current_user
from ..db import get_db
from ..models.user import User
router = APIRouter(prefix="/mfa", tags=["mfa"])
class VerifyIn(BaseModel):
    code: str
@router.get("/setup")
def setup(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32(); db.add(user); db.commit()
    totp = pyotp.TOTP(user.mfa_secret); uri = totp.provisioning_uri(name=user.username, issuer_name="AI-Logs")
    return {"secret": user.mfa_secret, "otpauth": uri}
@router.post("/enable")
def enable(payload: VerifyIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.mfa_secret: raise HTTPException(400, "Setup first")
    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(payload.code, valid_window=1): raise HTTPException(400, "Code invalid")
    user.mfa_enabled = True; db.add(user); db.commit(); return {"enabled": True}
@router.post("/disable")
def disable(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.mfa_enabled = False; user.mfa_secret = None; db.add(user); db.commit(); return {"enabled": False}
