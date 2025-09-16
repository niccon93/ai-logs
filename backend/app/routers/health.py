from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health(): return {"status":"ok"}

@router.get("/live")
def live(): return {"status":"alive"}

@router.get("/ready")
def ready(): return {"status":"ready"}
