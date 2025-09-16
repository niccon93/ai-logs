
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import os
from ..db import SessionLocal
from ..models.user import User
from ..security import create_access_token
router = APIRouter(tags=["auth-oidc"], prefix="/auth")
oauth = OAuth()
oidc_conf = {"client_id": os.getenv("OIDC_CLIENT_ID",""), "client_secret": os.getenv("OIDC_CLIENT_SECRET",""),
             "server_metadata_url": os.getenv("OIDC_DISCOVERY_URL",""), "client_kwargs": {"scope": "openid email profile"}}
if oidc_conf["client_id"] and oidc_conf["server_metadata_url"]:
    oauth.register(name="oidc", **oidc_conf)
@router.get("/oidc/login")
async def oidc_login(request: Request):
    if "oidc" not in oauth._clients: raise HTTPException(503, "OIDC not configured")
    redirect_uri = os.getenv("OIDC_REDIRECT_URI", str(request.url_for("oidc_callback")))
    return await oauth.oidc.authorize_redirect(request, redirect_uri)
@router.get("/oidc/callback")
async def oidc_callback(request: Request):
    if "oidc" not in oauth._clients: raise HTTPException(503, "OIDC not configured")
    token = await oauth.oidc.authorize_access_token(request); userinfo = token.get("userinfo") or {}
    email = userinfo.get("email"); if not email: raise HTTPException(400, "OIDC missing email")
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter((User.email==email)|(User.username==email)).first()
        if not user: user = User(username=email, email=email, role="viewer", password_hash="!"); db.add(user); db.commit(); db.refresh(user)
        jwt = create_access_token({"sub": str(user.id), "role": (getattr(user.role,'value', user.role))})
        front = os.getenv("FRONTEND_URL", "/"); return RedirectResponse(url=f"{front}#token={jwt}")
    finally: db.close()
