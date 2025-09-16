from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from ..deps import get_current_user, require_admin
from ..services.parse_drain import parse_lines
from ..workers.celery_app import enqueue_parse

router = APIRouter(prefix="/ingest", tags=["ingest"])

class LinesIn(BaseModel):
    lines: List[str]

@router.post("/preview")
def preview(data: LinesIn, _=Depends(get_current_user)):
    return {"parsed": parse_lines(data.lines)}

@router.post("/queue")
def queue(data: LinesIn, _=Depends(require_admin)):
    task_id = enqueue_parse.apply_async(kwargs={"lines": data.lines}, queue="parse").id
    return {"task_id": task_id}
