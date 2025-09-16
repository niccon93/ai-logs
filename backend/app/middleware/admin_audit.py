
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ..db import SessionLocal
class AdminAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        try:
            user = getattr(request.state, "user", None)
            role_val = getattr(getattr(user, "role", None), "value", None) if user else None
            if role_val in ("admin",) or request.method in ("POST","PUT","PATCH","DELETE"):
                db = SessionLocal()
                db.execute(
                    "INSERT INTO admin_audit_logs (ts,user_id,action,method,path,ip,details) VALUES (now(), :uid, :act, :m, :p, :ip, :det)",
                    {"uid": getattr(user, "id", None), "act": "request", "m": request.method, "p": request.url.path, "ip": request.client.host if request.client else None, "det": "{}"}
                )
                db.commit(); db.close()
        except Exception: pass
        return response
